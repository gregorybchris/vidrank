import { Nav } from "@/app/new/nav";
import "@/styles/globals.css";

type RootLayoutProps = {
  children: React.ReactNode;
};

export default async function RootLayout({ children }: RootLayoutProps) {
  return (
    <div className="min-w-screen min-h-screen p-5 font-manrope">
      <Nav>{children}</Nav>
    </div>
  );
}
