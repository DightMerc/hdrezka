from starlette.requests import Request

from app.api.schemas.requests.records import ContentRequestSchema
from app.clients.hdrezka import Player, PlayerSeries, PlayerMovie
from app.controllers import BaseController


class ContentController(BaseController):
    def __init__(self, request: Request):
        super(ContentController, self).__init__(
            request=request, schema=ContentRequestSchema
        )

    async def _call(self):
        await self._parse_request_data()
        self.request_data: ContentRequestSchema

        player: PlayerSeries | PlayerMovie = await Player(
            url_or_path=self.request_data.url
        )

        stream = await player.get_stream(
            season=self.request_data.season,
            episode=self.request_data.episode,
            translator_id=self.request_data.translator_id,
        )
        video = stream.video
        # print(await video.last_url)  # best quality (.m3u8)
        # print((await video[video.min].last_url).mp4, end="\n\n")  # worst quality (.mp4)

        return video.raw_data
