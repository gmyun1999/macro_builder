class BlockFunctionUseCase:
    def __init__(self) -> None:
        pass

    def update_process(self):
        """
        기존의 블럭함수를 수정하는
        """
        pass

    def create_process(self):
        """
        블럭함수를 새로 생성하는
        """
        pass

    def delete_process(self):
        """
        service 의 delete_block_function_with_closure_function 그대로 쓰면될듯?
        """
        pass

    def has_child_function(self):
        """
        function 이 삭제될때 이를 참조하고있는 child function이 있는지 체크하고
        사용자에게 삭제될수있음을 알려주는 용도
        """
        pass
