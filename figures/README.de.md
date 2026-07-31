# Abbildungen

Speichern Sie editierbare Quelldateien und finale LaTeX-Exporte in diesem
Verzeichnis.

- Verwenden Sie PDF für Vektorgrafiken und Diagramme.
- Verwenden Sie PNG für Rasterbilder mit ausreichender Auflösung.
- Vermeiden Sie JPEG bei Liniengrafiken und textreichen Abbildungen.
- Prüfen Sie jede Beschriftung in der tatsächlich verwendeten Größe.
- Verwenden Sie eindeutige Dateinamen wie `ap1-versuchsplan.pdf`.

Beispiel:

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{figures/ap1-versuchsplan.pdf}
  \caption{Kurze und eigenständig verständliche Bildunterschrift.}
  \label{fig:ap1}
\end{figure}
```
