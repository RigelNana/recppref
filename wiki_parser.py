import mwparserfromhell
import json
from typing import Dict, List, Any, Union
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ImprovedWikiTextParser:
    """
    改进的 MediaWiki 文本解析器，按照用户指定的格式输出。
    所有元素（文本和模板）按照在原始文档中的顺序排列。
    """
    
    def __init__(self):
        """初始化解析器"""
        self.section_stack = []  # 用于跟踪章节层级
        
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        解析单个 wiki 文件
        
        Args:
            file_path: wiki 文件路径
            
        Returns:
            解析后的 JSON 数据结构
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"解析文件: {file_path}")
            return self.parse_content(content, file_path)
            
        except Exception as e:
            logger.error(f"解析文件 {file_path} 时出错: {str(e)}")
            return {"error": str(e), "file": file_path}
    
    def parse_content(self, content: str, source_file: str = "") -> Dict[str, Any]:
        """
        解析 wikitext 内容，按顺序输出所有元素
        
        Args:
            content: wikitext 内容
            source_file: 源文件路径（用于调试）
            
        Returns:
            解析后的数据结构
        """
        try:
            # 解析 wikitext
            wikicode = mwparserfromhell.parse(content)
            
            # 按顺序解析所有节点
            parsed_content = self._parse_nodes_sequentially(wikicode.nodes)
            
            result = {
                "source_file": source_file,
                "content": parsed_content
            }
            
            return result
            
        except Exception as e:
            logger.error(f"解析内容时出错: {str(e)}")
            return {"error": str(e), "content_preview": content[:200]}
    
    def _parse_nodes_sequentially(self, nodes) -> List[Dict[str, Any]]:
        """
        按顺序解析所有节点
        
        Args:
            nodes: mwparserfromhell 节点列表
            
        Returns:
            解析后的节点列表
        """
        result = []
        current_text = ""
        
        for node in nodes:
            try:
                if hasattr(node, 'name'):  # 模板节点
                    # 先保存累积的文本
                    if current_text.strip():
                        result.append({
                            "type": "text",
                            "content": current_text.strip()
                        })
                        current_text = ""
                    
                    # 解析模板
                    template_data = self._parse_template(node)
                    result.append(template_data)
                    
                elif str(node).strip().startswith('=') and str(node).strip().endswith('='):
                    # 章节标题
                    # 先保存累积的文本
                    if current_text.strip():
                        result.append({
                            "type": "text",
                            "content": current_text.strip()
                        })
                        current_text = ""
                    
                    section_data = self._parse_section_header(str(node))
                    if section_data:
                        result.append(section_data)
                    
                else:
                    # 文本节点
                    node_text = str(node)
                    if node_text.strip():
                        current_text += node_text
                        
            except Exception as e:
                logger.warning(f"解析节点时出错: {str(e)}")
                # 将有问题的节点作为文本处理
                current_text += str(node)
        
        # 保存最后剩余的文本
        if current_text.strip():
            result.append({
                "type": "text",
                "content": current_text.strip()
            })
        
        return result
    
    def _parse_template(self, template) -> Dict[str, Any]:
        """
        解析单个模板，使用新的格式
        
        Args:
            template: mwparserfromhell 模板对象
            
        Returns:
            解析后的模板数据
        """
        try:
            template_data = {
                "type": "template",
                "name": str(template.name).strip(),
                "named_params": {}
            }
            
            # 解析参数 - 所有参数都放入 named_params
            for i, param in enumerate(template.params):
                param_value = self._parse_parameter_value(param.value)
                
                if param.name:
                    # 使用实际的参数名称（包括数字索引）
                    param_name = str(param.name).strip()
                    template_data["named_params"][param_name] = param_value
                else:
                    # 理论上不应该到这里，因为 mwparserfromhell 总是给参数分配名称
                    # 但以防万一，使用索引作为名称
                    template_data["named_params"][str(i + 1)] = param_value
            
            return template_data
            
        except Exception as e:
            logger.warning(f"解析模板时出错: {str(e)}")
            return {
                "type": "template",
                "name": "parse_error", 
                "error": str(e),
                "named_params": {}
            }
    
    def _parse_parameter_value(self, param_value) -> Union[str, Dict[str, Any], List[Any]]:
        """
        解析参数值，可能包含嵌套模板
        
        Args:
            param_value: 参数值对象
            
        Returns:
            解析后的参数值
        """
        try:
            param_str = str(param_value).strip()
            
            # 如果参数值包含模板语法
            if "{{" in param_str or param_str.startswith("="):
                try:
                    # 尝试解析为 wikicode
                    nested_wikicode = mwparserfromhell.parse(param_str)
                    
                    # 检查是否包含模板
                    templates = list(nested_wikicode.filter_templates())
                    if templates:
                        # 如果只有一个模板且没有其他内容，直接返回模板
                        if len(templates) == 1 and nested_wikicode.strip_code().strip() == "":
                            return self._parse_template(templates[0])
                        else:
                            # 包含多个元素，按顺序解析
                            return self._parse_nodes_sequentially(nested_wikicode.nodes)
                    
                except Exception as e:
                    logger.debug(f"解析嵌套内容时出错: {str(e)}")
            
            # 普通文本参数
            return param_str
            
        except Exception as e:
            logger.warning(f"解析参数值时出错: {str(e)}")
            return str(param_value)
    
    def _parse_section_header(self, header_text: str) -> Dict[str, Any]:
        """
        解析章节标题
        
        Args:
            header_text: 章节标题文本
            
        Returns:
            章节数据
        """
        try:
            header_text = header_text.strip()
            
            # 计算标题级别
            level = 0
            start_pos = 0
            while start_pos < len(header_text) and header_text[start_pos] == '=':
                level += 1
                start_pos += 1
            
            # 提取标题文本
            title = header_text[level:-level].strip()
            
            return {
                "type": "section",
                "level": level,
                "title": title
            }
            
        except Exception as e:
            logger.warning(f"解析章节标题时出错: {str(e)}")
            return None
    
    def parse_with_sections(self, content: str, source_file: str = "") -> Dict[str, Any]:
        """
        解析内容并按章节组织
        
        Args:
            content: wikitext 内容
            source_file: 源文件路径
            
        Returns:
            按章节组织的解析结果
        """
        try:
            # 先按顺序解析所有内容
            sequential_result = self.parse_content(content, source_file)
            
            if "error" in sequential_result:
                return sequential_result
            
            # 重新组织为章节结构
            organized_content = []
            current_section = None
            
            for item in sequential_result["content"]:
                if item["type"] == "section":
                    # 保存当前章节
                    if current_section is not None:
                        organized_content.append(current_section)
                    
                    # 开始新章节
                    current_section = {
                        "type": "section",
                        "level": item["level"],
                        "title": item["title"],
                        "content": []
                    }
                else:
                    # 添加到当前章节或顶级内容
                    if current_section is not None:
                        current_section["content"].append(item)
                    else:
                        organized_content.append(item)
            
            # 添加最后一个章节
            if current_section is not None:
                organized_content.append(current_section)
            
            return {
                "source_file": source_file,
                "content": organized_content
            }
            
        except Exception as e:
            logger.error(f"按章节解析时出错: {str(e)}")
            return {"error": str(e)}
    
    def save_to_json(self, data: Dict[str, Any], output_file: str) -> bool:
        """
        将解析结果保存为 JSON 文件
        
        Args:
            data: 要保存的数据
            output_file: 输出文件路径
            
        Returns:
            保存是否成功
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"结果已保存到: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"保存 JSON 文件时出错: {str(e)}")
            return False


def main():
    """主函数示例"""
    parser = ImprovedWikiTextParser()
    
    # 测试单个文件
    test_file = "/Users/rigelshrimp/cppref_migration/wikis/cpp/chrono/duration.wiki"
    
    print("=== 顺序解析结果 ===")
    result = parser.parse_file(test_file)
    parser.save_to_json(result, "sequential_output.json")
    
    print("=== 按章节组织结果 ===")
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    section_result = parser.parse_with_sections(content, test_file)
    parser.save_to_json(section_result, "sectioned_output.json")
    


if __name__ == "__main__":
    main()
