import json
import sys
import os
import html
from typing import List, Dict, Any, Set


def generate_props_string(props: Dict[str, Any]) -> str:
    items = []
    for key, value in props.items():
        if isinstance(value, bool):
            js_bool = str(value).lower()
            items.append(f"{key}={{{js_bool}}}")
        elif isinstance(value, (int, float)):
            items.append(f"{key}={{{value}}}")
        else:
            items.append(f'{key}="{value}"')
    return " ".join(items)

def generate_mdx_from_node(node: Dict[str, Any], components_used: Set[str], is_child_of_component: bool = False) -> str:
    node_type = node.get("type")
    
    if node_type == "text":
        content = node.get("content", "")
        unescaped_content = html.unescape(content)

        if is_child_of_component:
            return f"{{{json.dumps(unescaped_content)}}}"
        
        return unescaped_content
    
    if node_type == "component":
        component_name = node["component_name"]
        components_used.add(component_name)
        
        props_str = generate_props_string(node.get("props", {}))
        
        mdx_parts = [f"<{component_name} {props_str}".strip() + ">"]
        
        slots = node.get("slots", {})
        if "default" in slots:
            for child_node in slots["default"]:
                mdx_parts.append(generate_mdx_from_node(child_node, components_used, is_child_of_component=True))
        
        for slot_name, slot_nodes in slots.items():
            if slot_name != "default":
                
                mdx_parts.append(f'<span slot="{slot_name}">')
                for child_node in slot_nodes:
                    mdx_parts.append(generate_mdx_from_node(child_node, components_used, is_child_of_component=True))
                mdx_parts.append('</span>')


        mdx_parts.append(f"</{component_name}>")
        
        
        return "".join(mdx_parts)
        
    return ""

def main():
    if len(sys.argv) != 4:
        print("Usage: python generate_mdx.py <ir_input.json> <mdx_output_dir> <components_path>", file=sys.stderr)
        print("Example: python generate_mdx.py ir.json ./output src/components", file=sys.stderr)
        sys.exit(1)
        
    ir_input_path = sys.argv[1]
    mdx_output_dir = sys.argv[2]
    components_base_path = sys.argv[3]

    if not os.path.exists(ir_input_path):
        print(f"Error: Input file not found at {ir_input_path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(mdx_output_dir):
        print(f"Output directory not found. Creating it: {mdx_output_dir}")
        os.makedirs(mdx_output_dir)

    base_filename = os.path.splitext(os.path.basename(ir_input_path))[0]

    if base_filename.endswith('.ir'):
        base_filename = base_filename[:-3]
    mdx_output_path = os.path.join(mdx_output_dir, f"{base_filename}.mdx")


    with open(ir_input_path, 'r', encoding='utf-8') as f:
        ir_tree = json.load(f)
        
    components_used = set()
    mdx_content_parts = [generate_mdx_from_node(node, components_used, is_child_of_component=False) for node in ir_tree]
    mdx_content = "".join(mdx_content_parts)
    
    import_statements = [f'import {component} from "@/components/{component}.astro";' for component in sorted(list(components_used))]
    
    page_title = base_filename.replace('_', ' ').replace('-', ' ').title()
    
    frontmatter = f"""---
layout: '@/layouts/Layout.astro'
title: '{page_title}'
---
"""

    final_mdx = frontmatter + "\n".join(import_statements) + "\n\n" + mdx_content
    
    with open(mdx_output_path, 'w', encoding='utf-8') as f:
        f.write(final_mdx)
        
    print(f"Successfully generated MDX at {mdx_output_path}")

if __name__ == '__main__':
    main()
