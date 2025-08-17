import json
import tomllib
import sys
import os
from typing import List, Dict, Any, Union


IRNode = Dict[str, Any]
TextNode = Dict[str, str]
ComponentNode = Dict[str, Any]

def load_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, 'rb') as f:
        return tomllib.load(f)

def process_node_list(nodes: List[Dict[str, Any]], config: Dict[str, Any]) -> List[IRNode]:
    ir_nodes = []
    for node in nodes:
        node_type = node.get('type')
        if node_type == 'text':
            ir_nodes.append({
                "type": "text",
                "content": node.get('value', '')
            })
        elif node_type == 'template':
            ir_nodes.append(create_component_node(node, config))
    return ir_nodes

def create_component_node(template_node: Dict[str, Any], config: Dict[str, Any]) -> ComponentNode:
    template_name = template_node.get('name', '').strip()
    template_config = config.get(template_name)

    if not template_config:
        params = [f"{k}={v}" for k, v in template_node.get('named_params', {}).items()]
        return {
            "type": "text",
            "content": f"{{{{ {template_name} | {' | '.join(params)} }}}}"
        }

    component_name = template_config.get('component')
    props = template_config.get('intrinsic', {}).copy()
    slots = {}


    param_map = template_config.get('params', {})
    template_params = template_node.get('params', {})

    for param_key, slot_name in param_map.items():
        if param_key in template_params:
            param_value = template_params[param_key]
            if isinstance(param_value, dict) and 'type' in param_value:
                slots[slot_name] = process_node_list([param_value], config)
            elif isinstance(param_value, list):
                slots[slot_name] = process_node_list(param_value, config)
            else:
                slots[slot_name] = [{"type": "text", "content": str(param_value)}]

    return {
        "type": "component",
        "component_name": component_name,
        "props": props,
        "slots": slots
    }


def generate_ir_tree(sectioned_nodes: List[Dict[str, Any]], config: Dict[str, Any]) -> List[IRNode]:
    ir_root: List[IRNode] = []
    parent_stack: List[Union[List[IRNode], ComponentNode]] = [ir_root]

    for node in sectioned_nodes:
        current_parent_list = parent_stack[-1]
        if isinstance(current_parent_list, dict):
             current_parent_list = current_parent_list['slots'].setdefault('default', [])


        node_type = node.get('type')

        if node_type == 'text':
            ir_node = {
                "type": "text",
                "content": node.get('content', '')
            }
            current_parent_list.append(ir_node)

        elif node_type == 'section':
            section_ir_node = {
                "type": "component",
                "component_name": "Section",
                "props": {
                    "title": node.get("title", ""),
                    "level": node.get("level", 2)
                },
                "slots": {
                    "default": generate_ir_tree(node.get("content", []), config)
                }
            }
            current_parent_list.append(section_ir_node)
        
        elif node_type == 'template':
            template_name = node.get('name', '').strip()
            template_config = config.get(template_name, {})
            
            template_type = template_config.get('type')

            if template_type == 'standalone':
                ir_node = create_component_node(node, config)
                current_parent_list.append(ir_node)
            
            elif template_type == 'blockstart':
                ir_node = create_component_node(node, config)
                current_parent_list.append(ir_node)
                parent_stack.append(ir_node)

            elif template_type == 'blockend':
                if len(parent_stack) > 1:
                    parent_stack.pop()
                else:
                    print(f"Warning: Encountered a blockend '{template_name}' without a matching blockstart.", file=sys.stderr)

    return ir_root

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_ir.py <base_filename>", file=sys.stderr)
        print("This will use <base_filename>.json and generate <base_filename>.ir.json", file=sys.stderr)
        sys.exit(1)

    base_filename = sys.argv[1]
    config_path = 'config.toml'
    sectioned_json_path = f"{base_filename}"
    ir_output_path = f"{os.path.splitext(base_filename)[0]}.ir.json"
    config = load_config(config_path)
    
    with open(sectioned_json_path, 'r', encoding='utf-8') as f:
        sectioned_data = json.load(f)


    content_nodes = sectioned_data.get("content", [])
    ir_tree = generate_ir_tree(content_nodes, config)

    with open(ir_output_path, 'w', encoding='utf-8') as f:
        json.dump(ir_tree, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated IR at {ir_output_path}")

if __name__ == '__main__':
    main()
