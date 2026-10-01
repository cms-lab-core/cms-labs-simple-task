# CMS Labs Simple Task

[![CI](https://github.com/maintainer64/cms-labs-simple-task/actions/workflows/ci.yml/badge.svg)](https://github.com/maintainer64/cms-labs-simple-task/actions/workflows/ci.yml)
[![CodeQL](https://github.com/maintainer64/cms-labs-simple-task/actions/workflows/codeql.yml/badge.svg)](https://github.com/maintainer64/cms-labs-simple-task/actions/workflows/codeql.yml)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/maintainer64/cms-labs-simple-task?quickstart=1)

Это воспроизводимый пример задания CMS Labs и шаблон для будущих лабораторных работ. Codespace и локальный Dev Container запускают настоящий CMS Labs UI и весь Kubernetes-контур задания; дополнительные задания позже можно будет добавить по той же структуре. Задание содержит:

- Jupyter Notebook с описанием и заданиями;
- topology для локального Containerlab и шаблон для Clabgate/Clabernetes;
- изолированное окружение сетевых узлов;
- имя отдельного checker, возвращающего структурированный JSON-отчёт;
- автоматические проверки репозитория и полного жизненного цикла лаборатории.

## Быстрый старт в GitHub Codespaces

1. Нажмите **Open in GitHub Codespaces**.
2. Дождитесь сообщения `CMS Labs environment is ready` в терминале.
3. Codespaces создаст локальный kind-кластер и откроет CMS Labs frontend на порту `18080`.
4. Войдите как `admin@admin.com` с паролем `admin`. Demo-ссылка уже содержит идентификатор попытки.
5. На странице сессии дождитесь готовности topology и JupyterLab. Топология открывает встроенные ttyd-терминалы узлов, кнопка JupyterLab — рабочую тетрадь, кнопка «Проверить» — общий checker.

Codespace автоматически запускает:

- локальный kind и Clabernetes;
- настоящий `cms-labs-api` backend и CMS Labs frontend;
- две реплики Clabgate;
- MySQL с demo-пользователем, routing и попыткой;
- topology из двух узлов в отдельном namespace;
- `ghcr.io/maintainer64/cms-labs-jupyter:1.0.0`;
- `ghcr.io/maintainer64/cms-labs-checker:1.0.1` по кнопке проверки.

Наружу публикуется только frontend. Jupyter и ttyd остаются namespace-local и доступны через авторизованный proxy Clabgate с cookie, ограниченной одной сессией.

## Запуск на компьютере

Рекомендуемый способ одинаков для Linux, macOS и Windows:

1. Установите Docker и Visual Studio Code.
2. Установите расширение **Dev Containers**.
3. Клонируйте репозиторий и откройте его в VS Code.
4. Выполните `Dev Containers: Rebuild and Reopen in Container`.

После сборки окружение поднимется автоматически. Управлять им можно командами:

```bash
./scripts/demo up      # поднять полный CMS Labs контур
./scripts/demo status  # показать pods и topology
./scripts/demo open    # вывести demo URL
./scripts/demo down    # удалить локальный kind-кластер
```

Если порт `18080` уже занят, задайте другой: `CMS_LABS_FRONTEND_PORT=18081 ./scripts/demo up`.

На Linux с Docker команды можно запускать напрямую. Launcher при необходимости устанавливает закреплённые версии kind, kubectl и Helm. Облегчённый runner `./scripts/lab` оставлен для быстрой разработки checker и topology без CMS frontend.

## Текущая лабораторная работа

| Модуль | Тип | Тема | Среда | Проверка |
|---|---|---|---|---|
| `task` | `network-lab` | Автоматизация SSH и мониторинг SNMP | Jupyter + Containerlab/Clabernetes | `automatic-checker` |

Описание задания и шаги выполнения находятся в [`task/README.md`](task/README.md). Рабочая тетрадь — [`task.ipynb`](task/task.ipynb), контракт загрузки — [`task/lab.json`](task/lab.json). [`catalog.json`](catalog.json) оставлен как будущий registry шаблонов.

## Контур задания

Локальный runner воспроизводит те же три артефакта, которые использует production:

- Clabgate читает `topology.template.yaml` и создаёт topology в namespace попытки;
- Jupyter запускается из общего standalone-образа;
- `TEST_PATH=sdn_lab_5` выбирает пакет `labs/sdnlab5` в общем checker-образе.

В Codespace используется тот же session-протокол, что и в production. Отличаются только demo-аутентификация и локальная база: Moodle/LTI заменён заранее созданной попыткой `00000000-0000-0000-0000-000000000000`.

Версия шаблона `v1.0.3` закрепляет API `1.1.3`, Clabernetes fork `0.8.0-4`, Jupyter `1.0.0`, checker `1.0.1` и node image `1.0.3`. Тег `latest` публикуется для разработки, но воспроизводимый контур его не использует.

Внутри директории модуля единственным файлом `.yaml/.yml` является production-манифест. Это важно: Clabgate рекурсивно собирает все YAML из `labs_path` и применяет их как Kubernetes-ресурсы. Локальная topology поэтому имеет расширение `.clab`, а метаданные — `.json`.
