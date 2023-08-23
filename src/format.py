import os


class tformatting:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    DIM = "\033[2m"


def print_status(countdown, time, status, update_time):
    color = ""

    match status:
        case "*":
            color = ""
        case "-":
            color = tformatting.WARNING
        case "+":
            color = tformatting.FAIL

    print(
        "Next bus leaves in "
        + str(countdown)
        + " minutes at "
        + f"{color}"
        + time.split(" ")[0]
        + f"{tformatting.ENDC}"
        + "\n"
        + f"{tformatting.DIM}"
        + "Last updated at "
        + update_time
        + f"{tformatting.ENDC}"
    )


def print_error(res):
    print("\nERROR: [" + str(res.status_code) + "] " + res.reason + "\n")
