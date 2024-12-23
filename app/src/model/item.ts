export interface ItemGroup {
  name: string;
  count: number;
  items: string[];
}

export interface Item {
  id: string;
  name: string;
  description: string | null;
  quality: number | null;
  content: string;
  unlock: string | null;
  type: string | null;
  item_pool: string | null;
  recharge_time: string | null;
  position: [number, number];
}
