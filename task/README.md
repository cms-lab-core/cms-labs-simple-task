# Пример задания CMS Labs

Это самостоятельный пример задания CMS Labs: описание, Jupyter Notebook, topology, отдельный checker и одинаковый сценарий для Codespaces и production Clabgate.

## Цель

С помощью Python и `paramiko` назначить IPv4-адреса двум Linux-based сетевым узлам, проверить связность и прочитать системные данные через SNMP.

```text
r1 eth1 (10.50.0.1/30) <------> (10.50.0.2/30) eth1 s1
```

Служебная management-сеть создаётся Containerlab автоматически и не оценивается.

## Доступ к узлам

| Узел | Имя внутри лаборатории | Пользователь | Пароль | SNMP community |
|---|---|---|---|---|
| Router | `clab-simple-task-r1` | `student` | `student` | `public` |
| Switch | `clab-simple-task-s1` | `student` | `student` | `public` |

В Kubernetes notebook автоматически использует сервисы `<namespace>-r1` и `<namespace>-s1`; менять код для production не требуется.

## Задание

1. Откройте `task.ipynb`.
2. Подключитесь к обоим узлам по SSH.
3. Настройте `10.50.0.1/30` на `r1:eth1` и `10.50.0.2/30` на `s1:eth1`.
4. Проверьте ICMP-связность в обе стороны.
5. Получите `sysName.0` обоих узлов по SNMP.
6. В CMS Labs захватите ICMP на `r1:eth1` через `%%capture_traffic` и повторно
   откройте сохранённый PCAP через `%view_traffic`.
7. Запустите из терминала `./scripts/lab check`.

Итоговый checker оценивает пять пунктов: оба адреса, связность, SSH и SNMP. Отчёт соответствует JSON-контракту, который Clabgate отправляет в CMS/Moodle/LTI.

## Файлы

- `task.ipynb` — описание задания и рабочая тетрадь студента;
- `topology.clab` — локальный Containerlab/Codespaces; нестандартное расширение не даёт Clabgate применить файл как Kubernetes-манифест;
- `topology.template.yaml` — production-шаблон Clabernetes;
- `terminal.template.yaml` — короткая декларация terminal targets; установленный в кластере controller создаёт broker, RBAC, Services и NetworkPolicy;
- `capture.template.yaml` — декларация лимитов namespace-local захвата трафика и временного PCAP-хранилища;
- `node/` — открытый образ учебного Linux-узла;
- `lab.json` — метаданные обнаружения лаборатории.

Команда terminal задаётся отдельно для каждого target. В этом задании оба Alpine-узла используют
`/bin/ash -l`; в смешанной topology SR Linux может использовать `sr_cli`, а Linux-PC — `/bin/bash -l`.

Раздел захвата доступен в Kubernetes-сессии CMS Labs. В обычном Codespace нет
Clabernetes `clabwire` и Capture API, поэтому основное задание там выполняется
без двух дополнительных PCAP-ячеек.
