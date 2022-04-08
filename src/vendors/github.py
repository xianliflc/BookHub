DEFAULT_BRANCH = 'master'
DEFAULT_BASE_URL = 'https://github.com'
DEFAULT_RAW_BASE_URL ='https://raw.githubusercontent.com/'

class Github:

    @staticmethod
    def getRemoteUrl(
        repo_url: str,
        relative_url: str,
        branch : str = DEFAULT_BRANCH,
        base_raw_url: str = DEFAULT_RAW_BASE_URL,
        base_url: str = DEFAULT_BASE_URL
    ) -> str:
        partial_url = repo_url.replace(base_url, base_raw_url)
        return partial_url + '/' + branch + '/' + relative_url 
