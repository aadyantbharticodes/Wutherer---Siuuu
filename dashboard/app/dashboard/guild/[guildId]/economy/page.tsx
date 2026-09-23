"use client";

import { Card, CardContent } from "@/components/ui/card";
import { SectionHeader } from "@/components/ui/section-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Alert } from "@/components/ui/alert";
import { ShoppingBag } from "lucide-react";

export default function EconomyStorePage() {
  return (
    <div className="space-y-5">
      <SectionHeader
        title="Economy & Store"
        description="Server credits, wallets, and the purchasable role catalog."
      />

      <Alert variant="info">
        The bot does not expose a store management API, so this dashboard cannot list or edit live
        store items. Manage the catalog in Discord with shop commands — nothing below is fabricated
        as live data.
      </Alert>

      <Card>
        <CardContent className="space-y-3 pt-4">
          <h2 className="text-sm font-semibold text-white">Manage the store in Discord</h2>
          <ul className="space-y-1.5 text-sm text-slate-400">
            <li>
              <code className="rounded bg-surface px-1.5 py-0.5 font-mono text-xs text-primary-light">shop</code>
              {" — display the server item and role catalog"}
            </li>
            <li>
              <code className="rounded bg-surface px-1.5 py-0.5 font-mono text-xs text-primary-light">buy {"<item_id>"}</code>
              {" — purchase an item with wallet credits"}
            </li>
            <li>
              <code className="rounded bg-surface px-1.5 py-0.5 font-mono text-xs text-primary-light">inventory [member]</code>
              {" — inspect personal items and badges"}
            </li>
            <li>
              <code className="rounded bg-surface px-1.5 py-0.5 font-mono text-xs text-primary-light">shop add role {"<@role> <price> [desc]"}</code>
              {" — list a purchasable role (Administrator)"}
            </li>
            <li>
              <code className="rounded bg-surface px-1.5 py-0.5 font-mono text-xs text-primary-light">balance · daily · work · pay</code>
              {" — earn and move credits"}
            </li>
          </ul>
        </CardContent>
      </Card>

      <Card>
        <EmptyState
          icon={ShoppingBag}
          title="No live store data here"
          description="Once a store API is available, purchasable roles and inventory will be listed here with real prices and stock. Until then, use the Discord commands above."
        />
      </Card>
    </div>
  );
}
