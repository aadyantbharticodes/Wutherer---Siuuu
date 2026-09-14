/// <reference types="node" />

declare namespace JSX {
  interface Element extends React.ReactElement<any, any> {}
  interface ElementClass extends React.Component<any> {
    render(): React.ReactNode;
  }
  interface ElementAttributesProperty {
    props: {};
  }
  interface ElementChildrenAttribute {
    children: {};
  }
  interface IntrinsicElements {
    [elemName: string]: any;
  }
}

declare namespace React {
  export type ReactNode =
    | ReactElement
    | string
    | number
    | Iterable<ReactNode>
    | ReactPortal
    | boolean
    | null
    | undefined;

  export type ReactElement<P = any, T extends string | JSXElementConstructor<any> = string | JSXElementConstructor<any>> = {
    type: T;
    props: P;
    key: string | number | null;
  };

  export type ReactPortal = ReactElement & {
    children: ReactNode;
  };

  export type JSXElementConstructor<P> =
    | ((props: P) => ReactElement<any, any> | null)
    | (new (props: P) => Component<any, any>);

  export type ComponentType<P = {}> = ComponentClass<P> | FunctionComponent<P>;
  export type FunctionComponent<P = {}> = (props: P) => ReactElement<any, any> | null;
  export type FC<P = {}> = FunctionComponent<P>;

  export interface ComponentClass<P = {}, S = ComponentState> {
    new (props: P, context?: any): Component<P, S>;
  }

  export class Component<P = {}, S = {}> {
    constructor(props: P);
    state: Readonly<S>;
    props: Readonly<P>;
    render(): ReactNode;
  }

  export interface ComponentState {}

  export interface HTMLAttributes<T> {
    className?: string;
    style?: any;
    id?: string;
    key?: any;
    ref?: any;
    children?: ReactNode;
    onClick?: (event: any) => void;
    onChange?: (event: any) => void;
    onSubmit?: (event: any) => void;
    [key: string]: any;
  }

  export interface ButtonHTMLAttributes<T> extends HTMLAttributes<T> {
    disabled?: boolean;
    type?: "submit" | "reset" | "button";
  }

  export interface AnchorHTMLAttributes<T> extends HTMLAttributes<T> {
    href?: string;
    target?: string;
    rel?: string;
  }

  export interface SVGProps<T> extends HTMLAttributes<T> {
    width?: string | number;
    height?: string | number;
    viewBox?: string;
    fill?: string;
    stroke?: string;
    strokeWidth?: string | number;
  }

  export type ElementRef<C> = any;
  export type ComponentPropsWithoutRef<T> = any;

  export type ForwardRefExoticComponent<P> = {
    (props: P): ReactElement | null;
    displayName?: string;
  };

  export function forwardRef<T, P = {}>(
    render: (props: P, ref: any) => ReactElement | null
  ): ForwardRefExoticComponent<P & { ref?: any }>;

  export function useState<T>(initialState: T | (() => T)): [T, (value: T | ((prev: T) => T)) => void];
  export function useEffect(effect: () => void | (() => void), deps?: any[]): void;
  export function useMemo<T>(factory: () => T, deps: any[] | undefined): T;
  export function useCallback<T extends (...args: any[]) => any>(callback: T, deps: any[]): T;
  export function useRef<T>(initialValue?: T): { current: T };
  export function createContext<T>(defaultValue: T): any;
  export function useContext<T>(context: any): T;
}

declare module "react" {
  export = React;
}

declare module "react/jsx-runtime" {
  export const jsx: any;
  export const jsxs: any;
  export const Fragment: any;
}

declare module "react/jsx-dev-runtime" {
  export const jsxDEV: any;
  export const Fragment: any;
}

declare module "react-dom" {
  export const render: any;
  export const hydrate: any;
}

declare module "next" {
  export type Metadata = {
    title?: string;
    description?: string;
    [key: string]: any;
  };
  export default function next(options?: any): any;
}

declare module "next/link" {
  import React from "react";
  export interface LinkProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
    href: string;
    as?: string;
    replace?: boolean;
    scroll?: boolean;
    shallow?: boolean;
    passHref?: boolean;
    prefetch?: boolean;
    locale?: string | false;
    children?: React.ReactNode;
  }
  const Link: React.FC<LinkProps>;
  export default Link;
}

declare module "next/navigation" {
  export function useParams(): Record<string, string | string[]>;
  export function usePathname(): string;
  export function useRouter(): {
    push(href: string): void;
    replace(href: string): void;
    refresh(): void;
    back(): void;
    forward(): void;
    prefetch(href: string): void;
  };
  export function useSearchParams(): URLSearchParams;
}

declare module "lucide-react" {
  import React from "react";
  export interface LucideProps extends React.SVGProps<SVGSVGElement> {
    size?: string | number;
    color?: string;
    strokeWidth?: string | number;
    className?: string;
  }
  export type LucideIcon = React.FC<LucideProps>;
  export const Shield: LucideIcon;
  export const ShieldCheck: LucideIcon;
  export const Sparkles: LucideIcon;
  export const Zap: LucideIcon;
  export const Bot: LucideIcon;
  export const ArrowRight: LucideIcon;
  export const Lock: LucideIcon;
  export const Server: LucideIcon;
  export const Users: LucideIcon;
  export const LogIn: LucideIcon;
  export const LayoutDashboard: LucideIcon;
  export const ShieldAlert: LucideIcon;
  export const Sliders: LucideIcon;
  export const Award: LucideIcon;
  export const Ticket: LucideIcon;
  export const Youtube: LucideIcon;
  export const Gamepad2: LucideIcon;
  export const Terminal: LucideIcon;
  export const Settings: LucideIcon;
  export const ArrowLeft: LucideIcon;
  export const CheckCircle2: LucideIcon;
  export const BarChart3: LucideIcon;
  export const ShoppingBag: LucideIcon;
  export const Archive: LucideIcon;
  export const MessageSquare: LucideIcon;
  export const Layers: LucideIcon;
  export const UserPlus: LucideIcon;
  export const Download: LucideIcon;
  export const AlertTriangle: LucideIcon;
  export const UserCheck: LucideIcon;
  export const Bell: LucideIcon;
  export const Plus: LucideIcon;
  export const Trash2: LucideIcon;
  export const ExternalLink: LucideIcon;
  export const Unlock: LucideIcon;
  export const CheckCircle: LucideIcon;
  export const XCircle: LucideIcon;
  export const Info: LucideIcon;
  export const X: LucideIcon;
  export const Inbox: LucideIcon;
  export const RefreshCw: LucideIcon;
}

declare module "@radix-ui/react-switch" {
  import React from "react";
  export const Root: any;
  export const Thumb: any;
}

declare module "@radix-ui/react-slot" {
  import React from "react";
  export const Slot: any;
  export const Slottable: any;
}

declare module "clsx" {
  export type ClassValue = any;
  export function clsx(...inputs: ClassValue[]): string;
}

declare module "tailwind-merge" {
  export function twMerge(...classLists: any[]): string;
}

declare module "sonner" {
  export const toast: any;
  export const Toaster: any;
}

declare module "next-auth" {
  export const getServerSession: any;
  export default function NextAuth(...args: any[]): any;
}

declare module "next-auth/react" {
  export const useSession: any;
  export const signIn: any;
  export const signOut: any;
  export const SessionProvider: any;
}

