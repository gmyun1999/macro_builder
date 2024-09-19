from jinja2 import Template

from macro_sheet.domain.block.action_block import ActionBlock
from macro_sheet.domain.block.block import Block
from macro_sheet.domain.block.condition_block import ConditionBlock
from macro_sheet.domain.block.control_block import ControlBlock
from macro_sheet.service.i_code_generator.i_block_code_generator import (
    IBlockCodeGenerator,
)


class Jinja2BlockCodeGenerator(IBlockCodeGenerator):
    def generate_block_code(self, block: Block) -> str:
        if isinstance(block, ControlBlock):
            return self._generate_control_code(block)
        elif isinstance(block, ActionBlock):
            return self._generate_action_code(block)
        elif isinstance(block, ConditionBlock):
            return self._generate_condition_code(block)
        else:
            return "# Unsupported block type"

    def _generate_control_code(self, block: ControlBlock) -> str:
        template_str = """
        {% if control_type == "while" %}
        while {{ condition }}:
            {{ body }}
        {% elif control_type == "if" %}
        if {{ condition }}:
            {{ body }}
        {% endif %}
        """
        template = Template(template_str)
        condition_code = "\n".join(
            self.generate_block_code(cond) for cond in block.conditions
        )
        body_code = "\n".join(self.generate_block_code(b) for b in block.body)
        return template.render(
            control_type=block.control_type, condition=condition_code, body=body_code
        )

    def _generate_action_code(self, block: ActionBlock) -> str:
        template_str = """
        # Action on {{ target }}: {{ action }}
        perform_{{ action }}({{ target }})
        """
        template = Template(template_str)
        return template.render(action=block.action, target=block.target)

    def _generate_condition_code(self, block: ConditionBlock) -> str:
        template_str = """
        if {{ condition }}:
            # Add condition logic
        """
        template = Template(template_str)
        return template.render(condition=f"{block.condition_type} == {block.value}")
