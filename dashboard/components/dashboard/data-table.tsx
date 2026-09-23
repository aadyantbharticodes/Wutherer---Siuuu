"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { EmptyState } from "@/components/ui/empty-state";
import { Search } from "lucide-react";

export interface DataTableColumn<T> {
  key: string;
  header: string;
  align?: "left" | "right";
  render: (row: T) => React.ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  rows: T[];
  columns: DataTableColumn<T>[];
  getRowKey: (row: T, index: number) => string | number;
  searchPlaceholder?: string;
  searchKeys?: (row: T) => string;
  emptyTitle: string;
  emptyDescription: string;
  emptyIcon?: React.ComponentType<{ className?: string }>;
  loading?: boolean;
  filters?: React.ReactNode;
}

export function DataTable<T>({
  rows,
  columns,
  getRowKey,
  searchPlaceholder = "Search…",
  searchKeys,
  emptyTitle,
  emptyDescription,
  emptyIcon,
  loading,
  filters,
}: DataTableProps<T>) {
  const [query, setQuery] = React.useState("");

  const visible = React.useMemo(() => {
    const term = query.trim().toLowerCase();
    if (!term || !searchKeys) return rows;
    return rows.filter((row) => searchKeys(row).toLowerCase().includes(term));
  }, [rows, query, searchKeys]);

  if (loading) {
    return (
      <div className="space-y-2 animate-pulse" aria-label="Loading table">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-12 rounded-md border border-card-border bg-surface" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
        {searchKeys && (
          <label className="relative block w-full sm:max-w-xs">
            <span className="sr-only">{searchPlaceholder}</span>
            <Search
              className="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-500"
              aria-hidden="true"
            />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={searchPlaceholder}
              className="h-9 w-full rounded-md border border-card-border bg-surface py-2 pl-9 pr-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-primary"
            />
          </label>
        )}
        {filters && <div className="flex flex-wrap items-center gap-2">{filters}</div>}
      </div>

      {visible.length === 0 ? (
        <div className="glass-card rounded-2xl border border-card-border p-4">
          <EmptyState
            icon={(emptyIcon as React.ComponentType<{ className?: string }>) ?? Search}
            title={query ? "No matches found" : emptyTitle}
            description={query ? "Try a different search term or clear the filters." : emptyDescription}
          />
        </div>
      ) : (
        <div className="glass-card overflow-hidden rounded-2xl border border-card-border p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-card-border bg-surface font-medium text-slate-400">
                <tr>
                  {columns.map((col) => (
                    <th
                      key={col.key}
                      className={cn("px-4 py-2.5", col.align === "right" && "text-right", col.className)}
                    >
                      {col.header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-card-border">
                {visible.map((row, i) => (
                  <tr key={getRowKey(row, i)} className="transition-colors hover:bg-surface-hover/50">
                    {columns.map((col) => (
                      <td
                        key={col.key}
                        className={cn("px-4 py-2.5", col.align === "right" && "text-right", col.className)}
                      >
                        {col.render(row)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="border-t border-card-border px-4 py-2 text-[11px] text-slate-500">
            Showing {visible.length} of {rows.length}
          </p>
        </div>
      )}
    </div>
  );
}
