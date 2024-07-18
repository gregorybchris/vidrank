import "@/styles/globals.css";
import { Nav } from "./nav";

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
