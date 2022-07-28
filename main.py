import subprocess
from simple_term_menu import TerminalMenu
from json import loads
from typing import List


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def run(action: str, flags: str = '', args = '') -> None:
    command = f"deno run {flags} app.ts {action} {args}"
    command = command.split(' ')
    command = list(filter(lambda x: x, command))
    for stdout in execute(command):
        print(stdout, end='')


def prompt_number(prompt_msg: str) -> int:
    while True:
        string = input(prompt_msg)
        try:
            string_int = int(string)
            return string_int
        except ValueError:
            print('Please enter an integer')


def main():
    with open('./constants/actions.ts', 'r') as f:
        es_mod = f.read()
        action_array_string = es_mod[es_mod.find('['):es_mod.find(']') + 1]
        action_array: List[str] = loads(action_array_string)
        main_menu = TerminalMenu(action_array)

        close_menu = False
        while not close_menu:
            action_index = main_menu.show()
            selected_action = action_array[action_index]

            if selected_action == "quit":
                close_menu = True
            elif selected_action == "prep":
                no_dirs = prompt_number(
                    'How many directories of files for data are there? ')
                run(selected_action, "--allow-run --allow-write --allow-read", no_dirs)
                close_menu = True
            elif selected_action == "train":
                run(selected_action, "--allow-run")
                close_menu = True
            elif selected_action == "run":
                run(selected_action)
                close_menu = True
            elif selected_action == "show":
                run(selected_action, "--allow-run --allow-net --allow-read")
                close_menu = True
            else:
                print("Run with: ", selected_action)
                run("deno run app.ts this_will_throw")


if __name__ == '__main__':
    main()
