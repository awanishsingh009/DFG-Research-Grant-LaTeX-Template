# Figures

Keep editable source artwork and the final LaTeX-ready exports here.

- Prefer PDF for vector diagrams and graphs.
- Use PNG for raster images at sufficient resolution.
- Avoid JPEG for line art and text-heavy scientific diagrams.
- Test every label at the final size used in the proposal.
- Use descriptive names such as `wp1_design.pdf`, not `final2-new.pdf`.

Example:

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{figures/wp1_design.pdf}
  \caption{Concise, self-contained caption.}
  \label{fig:wp1}
\end{figure}
```
