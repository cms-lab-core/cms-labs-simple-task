# Описание задания

`cms-labs-simple-task` содержит самостоятельный воспроизводимый пример задания CMS Labs. Это не каталог конкретных курсов: репозиторий можно использовать как шаблон и открывать одним из поддерживаемых способов:

```text
CMS_TASK_URL=https://github.com/cms-lab-core/cms-labs-simple-task
```

Описание задания находится в `task/README.md`, а рабочая тетрадь — в `task/task.ipynb`. Clabgate использует `task` как `labs_path`, закрепляет попытку на одном commit SHA и получает из него topology и метаданные согласованной версии.

Задание можно открыть:

- в GitHub Codespaces — кнопкой в корневом README;
- локально — через Dev Container и Containerlab;
- в CMS — через frontend, Clabgate session и Kubernetes namespace.

Во всех режимах используется один и тот же notebook и одна и та же topology. Отличается только способ запуска среды.

Codespaces и Dev Container устанавливают локальный CMS Labs dev-stack из Helm chart `.cms-labs/chart`. Chart включает базу, backend, Clabgate deployment, frontend, RBAC, JWT Secret и demo seed; Clabernetes, terminal и capture также устанавливаются как Helm releases. Production-контракт задания в `task/*.template.yaml` при этом остаётся неизменным.

## Типы

Контракт лаборатории описывает её по нескольким независимым признакам:

- `network-lab` — предметный тип: практическая работа с сетевыми узлами;
- `jupyter-notebook` — пользовательский интерфейс с заданием и кодом студента;
- `containerlab` — локальный topology runtime для Codespaces и Dev Container;
- `clabernetes` — Kubernetes runtime, разворачиваемый Clabgate;
- `automatic-checker` — автоматическая проверка с JSON-отчётом и оценкой.

Способы запуска перечисляются отдельно: `github-codespaces`, `local-devcontainer` и `clabgate-kubernetes`. Следующие работы можно будет добавлять в `modules/` без изменения контракта текущей работы.

## Содержание задания

Практическая работа знакомит с программной настройкой Linux-based сетевых узлов через SSH и чтением состояния по SNMP. Студент назначает адреса лабораторному каналу, проверяет связность и получает структурированный отчёт.

Типы: `network-lab`, `jupyter-notebook`, `containerlab`, `clabernetes`, `automatic-checker`.

В отличие от старой коллекции, пример не зависит от приватных Cisco IOL-образов или внутренней сети университета и полностью запускается в GitHub Codespaces.
