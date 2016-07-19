from WotStats import WotStatService


def main():
    wot_service = WotStatService()
    wot_service.process_user_stats()


if __name__ == '__main__':
    main()
