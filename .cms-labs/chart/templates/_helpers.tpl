{{- define "cms-labs-dev.labels" -}}
app.kubernetes.io/part-of: cms-labs
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | quote }}
{{- end }}

{{- define "cms-labs-dev.selectorLabels" -}}
app.kubernetes.io/name: {{ .component }}
app.kubernetes.io/instance: {{ .root.Release.Name }}
{{- end }}

{{- define "cms-labs-dev.image" -}}
{{ printf "%s:%s" .repository .tag }}
{{- end }}
