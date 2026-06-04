import requests
import logging
import time


logger = logging.getLogger(__name__)


def get_response(base_url: str, endpoint: str,  
                 params: dict | None = None, 
                 headers: dict | None = None, 
                 timeout: int=10,
                 retries: int=3,
                 backoff: int=3) -> requests.response:
    
    """Test connection to API."""

    url = f'{base_url}{endpoint}'

    # Loop for max connection retries to API
    for attempt in range(retries): 


        # Connection to API is succesful
        try:
            response = requests.get(url=url, headers=headers, params=params, timeout=timeout)
            # raise for status will throw an error for bad responses (4xx or 5xx)
            response.raise_for_status()
            logger.info(f'Response status code: {response.status_code}')
            logger.info("Request succesful.")
            return response.json()
        # Timeout reached
        except requests.Timeout:
            logger.warning("Request timeout reached.")
        # Capturing HTTP errors
        except requests.HTTPError as e:
            status_code = response.status_code
            logger.warning(f"HTTP Erros: {status_code}")

            # Rate limit error, retry
            if status_code == 429:
                logger.warning("Rate limit reached")
            
            # Temporary server errors retry
            elif status_code >= 500:
                logger.warning("Server error.")

            # No retry status code
            else:
                raise
        
        except requests.RequestException as e:
            logger.error(f"Connection error to api: {e}")

        # Exponential backoff
        sleep_time = backoff**attempt
        logger.info(f"Retrying in {sleep_time} seconds ...")
        time.sleep(sleep_time)
        
        

    raise Exception("Maximum connection attempts exceeded.")



