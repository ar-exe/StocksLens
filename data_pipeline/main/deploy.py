from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from main import data_pipeline
from config import settings

deployment = Deployment.build_from_flow(
    flow=data_pipeline,
    name='daily-run',
    schedule=CronSchedule(cron="0 7 * * 1-5"),
    parameters={'watchlist': settings.watchlist}
)
if __name__ == 'main':
    deployment.apply()
