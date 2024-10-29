while (filename.size > 400):
    while (filename.size > 200):
        while (filename.size > 100):
            if (filename.startswith("data")):
                # File Action: MOVE
                target_loc = "/deep/source/path"
                target_detail = "FILE_NAME"

                destination = "/deep/destination/path"

                print("MOVE 작업:", target_loc, "에서", destination, "로 이동")



