from starlette.requests import Request

from app.api.schemas.requests.records import RecordInfoRequestSchema
from app.clients.hdrezka import Player, PlayerSeries, PlayerMovie
from app.controllers import BaseController


class RecordInfoController(BaseController):
    def __init__(self, request: Request):
        super(RecordInfoController, self).__init__(
            request=request, schema=RecordInfoRequestSchema
        )

    async def _call(self):
        await self._parse_request_data()
        self.request_data: RecordInfoRequestSchema

        player: PlayerSeries | PlayerMovie = await Player(
            url_or_path=self.request_data.url
        )
        return dict(
            type=player.post.type,
            info=dict(
                rating=player.post.info.rating,
                places=player.post.info.places,
                release=player.post.info.release,
                country=player.post.info.country,
                director=player.post.info.director,
                genre=player.post.info.genre,
                quality=player.post.info.quality,
                translator=player.post.info.translator,
                age_rating=player.post.info.age_rating,
                duration=player.post.info.duration,
                characters=player.post.info.characters,
                fields=player.post.info.fields,
                title=player.post.info.title,
                orig_title=player.post.info.orig_title,
                poster=player.post.info.poster,
                description=player.post.info.description,
                slogan=player.post.info.slogan,
            ),
            translators=[
                dict(id=translator_id, name=translator_name)
                for translator_name, translator_id in player.post.translators.name_id.items()
            ],
            other_parts=player.post.other_parts_urls,
        )
