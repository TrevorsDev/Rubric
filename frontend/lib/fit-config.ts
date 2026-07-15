export type FitLevel = "strong" | "partial" | "poor";

export interface FitDisplay {
  label: string;
  color: string;
  border: string;
  bg: string;
}

export const fitConfig: Record<FitLevel, FitDisplay> = {
  strong: {
    label: "Strong Fit",
    color: "text-emerald-400",
    border: "border-emerald-800/50",
    bg: "bg-emerald-950/30",
  },
  partial: {
    label: "Partial Fit",
    color: "text-amber-400",
    border: "border-amber-800/50",
    bg: "bg-amber-950/30",
  },
  poor: {
    label: "Poor Fit",
    color: "text-red-400",
    border: "border-red-800/50",
    bg: "bg-red-950/30",
  },
};
