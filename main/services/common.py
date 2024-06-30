import abc
import json

from termcolor import cprint

from config.config import settings


class Service(abc.ABC):
    def __init__(self, data=None, context=None, **kwargs):
        self.attrs = data or {}
        self.context = context or {}

        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @abc.abstractmethod
    def process(self, *args, **kwagrs):
        """Business logic here"""
        pass


class UserConfigService(Service):
    __json_file_path = settings.BASE_DIR / "user_config.json"
    __error_file_not_found = "User config not found."
    
    @classmethod
    def get_data(cls) -> None:
        try:
            with open(cls.__json_file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(cls.__error_file_not_found)
    
    def _get_data(self) -> None:
        try:
            with open(self.__json_file_path, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(self.__error_file_not_found)
    
    def _set_user_data(self, data) -> None:
        try:
            with open(self.__json_file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            raise FileNotFoundError(self.__error_file_not_found)

    def _first_start_check(self) -> bool:
        is_configured_status = self.data["is_configured"]
        if is_configured_status is None:
            is_configured_status = False
        return is_configured_status
    
    def _first_configuration(self) -> None:
        helper_names = str(
            input("Type your helper name or several (format: robert,bob,robbie): ")
        ).lower()
        localization = input("Localization (format: ru-RU | ua-UA | en-US): ")
        
        if "," in helper_names:
            helper_names = helper_names.replace(" ", "").split(",")
        else:
            if localization in ["ru-RU", "ua-UA"]:
                helper_names = [
                    f"{helper_names}а",
                    f"{helper_names}у",
                    f"{helper_names}е",
                    f"{helper_names}и",
                ]
            else:
                helper_names = [helper_names]
        
        data = {
            "is_configured": True,
            "default": {
                "helper_names": helper_names,
                "localization": localization,
            }
        }
        
        self._set_user_data(data)
        cprint("Everithing is set!", "green")
        
    
    def process(self, *args, **kwagrs):
        self._get_data()
        if not self._first_start_check():
            self._first_configuration()