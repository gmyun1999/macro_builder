# your_app/services.py

from .models import Function, Worksheet, WorksheetFunction


def update_referenced_functions_for_worksheet(worksheet):
    referenced_ids = set()
    to_process = []

    def traverse(block):
        if isinstance(block, dict):
            if block.get("block_type") == "REFERENCE_BLOCK":
                ref_id = block.get("reference_id")
                if ref_id and ref_id not in referenced_ids:
                    referenced_ids.add(ref_id)
                    to_process.append(ref_id)
            for value in block.values():
                if isinstance(value, (dict, list)):
                    traverse(value)
        elif isinstance(block, list):
            for item in block:
                traverse(item)

    traverse(worksheet.main_block)
    traverse(worksheet.blocks)

    while to_process:
        current_id = to_process.pop()
        if current_id not in referenced_ids:
            referenced_ids.add(current_id)
            try:
                func = Function.objects.get(id=current_id)
                traverse(func.blocks)
            except Function.DoesNotExist:
                continue

    functions = Function.objects.filter(id__in=referenced_ids)

    WorksheetFunction.objects.filter(worksheet=worksheet).delete()
    new_mappings = [
        WorksheetFunction(worksheet=worksheet, function=func) for func in functions
    ]
    WorksheetFunction.objects.bulk_create(new_mappings)


def update_referenced_functions_for_function(function):
    referenced_ids = set()
    to_process = []

    def traverse(block):
        if isinstance(block, dict):
            if block.get("block_type") == "REFERENCE_BLOCK":
                ref_id = block.get("reference_id")
                if ref_id and ref_id not in referenced_ids:
                    referenced_ids.add(ref_id)
                    to_process.append(ref_id)
            for value in block.values():
                if isinstance(value, (dict, list)):
                    traverse(value)
        elif isinstance(block, list):
            for item in block:
                traverse(item)

    traverse(function.blocks)

    while to_process:
        current_id = to_process.pop()
        if current_id not in referenced_ids:
            referenced_ids.add(current_id)
            try:
                func = Function.objects.get(id=current_id)
                traverse(func.blocks)
            except Function.DoesNotExist:
                continue

    functions = Function.objects.filter(id__in=referenced_ids)

    worksheets = Worksheet.objects.filter(
        WorksheetFunction__function=function
    ).distinct()

    for worksheet in worksheets:
        WorksheetFunction.objects.get_or_create(worksheet=worksheet, function=function)
        for func in functions:
            WorksheetFunction.objects.get_or_create(worksheet=worksheet, function=func)
