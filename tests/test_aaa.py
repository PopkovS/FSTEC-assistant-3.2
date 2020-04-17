import logging
# import pytest

# add filemode="w" to overwrite
import string

#
# logging.basicConfig(filename="sample.log", level=logging.INFO)
#
# logging.debug("This is a debug message")
# logging.info("Informational message")
# logging.error("An error has happened!")

# @pytest.mark.parametrize('summary, owner, done',
#                          [('sleep', 'None', False),
#                           ('wake', 'brian', False),
#                           ('breathe', 'BRIAN', True),
#                           ('eat eggs', 'BrIaN', False),
#                           ])
def test_add_3():
#     """Демонстрирует параметризацию с несколькими параметрами."""
#     # task = Task(summary, owner, done)
#     # task_id = tasks.add(task)
#     # t_from_db = tasks.get(task_id)
#     # assert equivalent(t_from_db, task)
#     print("\nsummary: ", summary)
#     print("owner: ", owner)
#     print("done: ", done)

    # a = 9
    a = (9,2)
    print("")
    print(str(type(a)))