# CMS Labs Simple Task

[![CI](https://github.com/cms-lab-core/cms-labs-simple-task/actions/workflows/ci.yml/badge.svg)](https://github.com/cms-lab-core/cms-labs-simple-task/actions/workflows/ci.yml)
[![CodeQL](https://github.com/cms-lab-core/cms-labs-simple-task/actions/workflows/codeql.yml/badge.svg)](https://github.com/cms-lab-core/cms-labs-simple-task/actions/workflows/codeql.yml)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/cms-lab-core/cms-labs-simple-task?quickstart=1)

Это воспроизводимый пример задания CMS Labs и шаблон для будущих лабораторных работ. Codespace и локальный Dev Container запускают настоящий CMS Labs UI и весь Kubernetes-контур задания; дополнительные задания позже можно будет добавить по той же структуре. Задание содержит:

- Jupyter Notebook с описанием и заданиями;
- topology для локального Containerlab и шаблон для Clabgate/Clabernetes;
- отдельный namespace-local `cms-labs-terminal`, не требующий `tmux` или модификации узлов;
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

- локальный kind и официальный Clabernetes;
- настоящий `cms-labs-api` backend и CMS Labs frontend;
- две реплики Clabgate;
- MySQL с demo-пользователем, routing и попыткой;
- topology из двух узлов и отдельный terminal broker в namespace попытки;
- `ghcr.io/cms-lab-core/cms-labs-jupyter:latest`;
- `ghcr.io/cms-lab-core/cms-labs-checker:latest` по кнопке проверки.

Наружу публикуется только frontend. Jupyter и terminal Services остаются namespace-local и доступны через авторизованный proxy Clabgate с cookie, ограниченной одной сессией. NetworkPolicy разрешает вход в terminal Pod только из namespace системного proxy.

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

- Clabgate читает разрешённые namespaced-ресурсы из `task/*.yaml` и применяет их в namespace попытки;
- `topology.template.yaml` описывает только topology, а `terminal.template.yaml` независимо и целиком описывает `cms-labs-terminal`, его конфигурацию, RBAC, NetworkPolicy и Services `r1-terminal`/`s1-terminal`;
- Jupyter запускается из общего standalone-образа;
- `TEST_PATH=sdn_lab_5` выбирает пакет `labs/sdnlab5` в общем checker-образе.

В Codespace используется тот же session-протокол, что и в production. Отличаются только demo-аутентификация и локальная база: Moodle/LTI заменён заранее созданной попыткой `00000000-0000-0000-0000-000000000000`.

Полный контур использует официальный Clabernetes `0.8.0` и `cms-labs-terminal:1.0.0`. Terminal broker подключается к узлам через Kubernetes exec и переживает перезагрузку браузерной вкладки без `tmux` внутри учебного устройства.

Файлы `*.template.yaml` являются production-манифестами задания. Clabgate рекурсивно находит только этот суффикс, пропускает ограниченный список namespaced-ресурсов, валидирует весь набор до первой записи и применяет его в namespace попытки. Поэтому demo/CI YAML из других каталогов не попадёт в сессию, локальная topology имеет расширение `.clab`, а метаданные — `.json`.
