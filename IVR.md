# Anatomy of an IVR

Every IVR is defined by 2 files:

1. `Schema`: This is a json file placed under `schemas`. Schema file provides your IVR configuration.
2. `Webhook`: Currently webhooks can only be written in `Python` language. All webhook code is placed under `webhooks`.

3. Above command has generate following 2 files:

   - `schemas/calculator.json`
   - `webhooks/calculator.py`

   Lets take a look at these generated files.

4. `schemas/calculator.json`

   ```json
   {
     "groups": [],
     "devices": [],
     "phones": [],
     "ivrs": [
       {
         "name": "calculator",
         "webhook": true
       }
     ]
   }
   ```

   - Generated schema defines 1-IVR named `calculator`
   - `calculator` is marked as `webhook` enabled i.e. code within `JaxlIVRCalculatorWebhook` class will drive this IVR.

5. `webhooks/calculator.py`

   ```python
   class JaxlIVRCalculatorWebhook(BaseJaxlIVRWebhook):
       """calculator.json webhook implementation."""

        @staticmethod
        def config() -> ConfigPathOrDict:
            return Path(__file__).parent.parent / "schemas" / "calculator.json"

        def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
            raise NotImplementedError()

        def teardown(self, request: JaxlIVRRequest) -> None:
            raise NotImplementedError()

        def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
            raise NotImplementedError()

        def stream(
            self,
            request: JaxlIVRRequest,
            chunk_id: int,
            sstate: Any,
        ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
            raise NotImplementedError()
   ```

   - `setup`: This method is called when a call is received for an IVR configured as `webhook=true`
   - `teardown`: This method is called when a call finishes
   - `handle_option`: This method must respond to inputs (options) chosen by the user in an active call
   - `stream`: This method is only called when prior a `JaxlIVRResponse` contained `stream=<interval>`. Note that:
     - All responses returned by `stream` must also include `stream=<interval>`
     - Passing `stream=None` will break the stream and flow will proceed to the next steps in the IVR flow
     - `chunk_id` is an integer which starts from 0 and incremented by 1 when `stream` method is repeatedly called
     - `stream` method must return a 2-tuple where 1st element is the internal state that you want to persist between subsequent calls to the `stream` method. 2nd element is `JaxlIVRResponse`.
