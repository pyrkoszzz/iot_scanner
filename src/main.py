from modules.input_module import InputHandler


def main():
    input_handler = InputHandler()
    ip_ranges = input_handler.get_ip_ranges()
    print(ip_ranges)


if __name__ == "__main__":
    main()
