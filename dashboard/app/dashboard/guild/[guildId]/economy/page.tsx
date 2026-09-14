"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { SectionHeader } from "@/components/ui/section-header";
import { EmptyState } from "@/components/ui/empty-state";
import { ShoppingBag, Trash2 } from "lucide-react";
import { ShopItem } from "@/types";

export default function EconomyStorePage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [items, setItems] = useState<ShopItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [itemName, setItemName] = useState("");
  const [itemPrice, setItemPrice] = useState("");
  const [itemDesc, setItemDesc] = useState("");

  useEffect(() => {
    setItems([
      {
        item_id: 1,
        guild_id: parseInt(guildId) || 0,
        name: "VIP Supporter Role",
        description: "Special badge and access to exclusive VIP lounge channels.",
        price: 5000,
        item_type: "role",
        stock: -1,
        enabled: true,
      },
      {
        item_id: 2,
        guild_id: parseInt(guildId) || 0,
        name: "Double XP Token",
        description: "2x multiplier on text and voice XP progression for 24 hours.",
        price: 2500,
        item_type: "consumable",
        stock: 50,
        enabled: true,
      },
      {
        item_id: 3,
        guild_id: parseInt(guildId) || 0,
        name: "Custom Vanity Color",
        description: "Allows custom role color hex code change.",
        price: 10000,
        item_type: "custom",
        stock: 10,
        enabled: true,
      },
    ]);
    setLoading(false);
  }, [guildId]);

  const handleAddItem = () => {
    const priceNum = parseInt(itemPrice);
    if (!itemName.trim() || isNaN(priceNum) || priceNum <= 0) return;

    const newItem: ShopItem = {
      item_id: Date.now(),
      guild_id: parseInt(guildId) || 0,
      name: itemName.trim(),
      description: itemDesc.trim() || "No description.",
      price: priceNum,
      item_type: "custom",
      stock: -1,
      enabled: true,
    };
    setItems([...items, newItem]);
    setItemName("");
    setItemPrice("");
    setItemDesc("");
  };

  const handleDeleteItem = (id: number) => {
    setItems(items.filter((i) => i.item_id !== id));
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Economy & Store"
        description="Configure purchasable roles, inventory items, and credit costs."
      />

      <Card>
        <CardHeader>
          <CardTitle>List Store Item</CardTitle>
          <CardDescription>Configure item title, credit cost, and perk details</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Item Name</label>
              <Input
                type="text"
                value={itemName}
                onChange={(e) => setItemName(e.target.value)}
                placeholder="e.g. Champion Role"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs text-slate-400">Price (Credits)</label>
              <Input
                type="number"
                value={itemPrice}
                onChange={(e) => setItemPrice(e.target.value)}
                placeholder="e.g. 5000"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs text-slate-400">Description</label>
              <Input
                type="text"
                value={itemDesc}
                onChange={(e) => setItemDesc(e.target.value)}
                placeholder="Perks and description..."
              />
            </div>
          </div>

          <div className="flex justify-end pt-1">
            <Button size="sm" onClick={handleAddItem}>List Item</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Store Catalog ({items.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {items.length === 0 ? (
            <EmptyState
              icon={ShoppingBag}
              title="No Store Items"
              description="Add an item to the store catalog above."
            />
          ) : (
            <div className="divide-y divide-card-border">
              {items.map((item) => (
                <div key={item.item_id} className="py-3 flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-white">{item.name}</span>
                      <Badge variant="warning">{item.price.toLocaleString()} Credits</Badge>
                      <Badge variant="default">{item.item_type}</Badge>
                    </div>
                    <p className="text-xs text-slate-400">{item.description}</p>
                  </div>

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDeleteItem(item.item_id)}
                    className="text-slate-500 hover:text-red-400"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
