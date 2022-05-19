broker_url = "amqp://tronmanager:dYvca5-sibcur-pydpec@129.154.59.231:5672/TronManager"
result_backend = "redis://manuel71:P9661144!@152.67.199.109:16379/10"

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]  # JSON을 제외한 다른 content 설정들은 무시
timezone = "Asia/Seoul"
enable_utc = True

task_routes = {
    "tron.tasks.add": "low-priority",
}

task_annotations = {
    "tron.tasks.add": {"rate_limit": "10/m"},
}
