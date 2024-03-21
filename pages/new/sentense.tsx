`use client`;
import { Link } from "@nextui-org/link";
import { Snippet } from "@nextui-org/snippet";
import { Code } from "@nextui-org/code";
import { button as buttonStyles } from "@nextui-org/theme";
import { siteConfig } from "@/config/site";
import { title, subtitle } from "@/components/primitives";
import { GithubIcon } from "@/components/icons";
import DefaultLayout from "@/layouts/default";
import Product from "@/components/product";

export default function IndexPage() {
	return (
		<DefaultLayout>
			<section className="flex flex-col gap-4 py-8 md:py-10 relative w-3/4" style={{ left: '18%' }}>
                <h1 className={title()}>读后续写润色</h1>
			</section>
		</DefaultLayout>
	);
}
