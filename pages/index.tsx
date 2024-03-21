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
			<section className="flex flex-col gap-4 py-8 md:py-10 relative" style={{ marginLeft: "18%", marginRight: "18%" }}>
				<div className="max-w-lg">
					<h1 className={title()}>It's time to&nbsp;</h1>
					<h1 className={title({ color: "violet" })}>enhance&nbsp;</h1>
					<br />
					<h1 className={title()}>
						your writing
					</h1>
					<br />
					<h1 className={title()}>
						with&nbsp;
					</h1>
					<h1 className={title({ color: "violet" })}>AI.</h1>
				</div>
				<div className="max-w-lg relative">
					<h4 className={subtitle({ class: "mt-4" })}>
						由目前最先进的人工智能模型驱动，拓展写作的边界。
					</h4>
				</div>
				<div className="flex gap-3">
					<Link
						isExternal
						className={buttonStyles({ variant: "bordered", radius: "full" })}
						href={siteConfig.links.github}
					>
						<GithubIcon size={20} />
						GitHub
					</Link>
				</div>
			</section>
			<section className="flex flex-col gap-4 py-8 md:py-10" style={{ marginLeft: "18%", marginRight: "18%" }}>
				<div className="max-w-lg">
					<h1 className={title()}>现在就开始。</h1>
				</div>
				<div className="max-w-lg relative">
					<h4 className={subtitle({ class: "mt-4" })}>
						查看我们的所有模型并使用。
					</h4>
				</div>
				<div className="flex gap-3">
					<Product name="读后续写润色" description="润色读后续写文章，提升文章整体质感。" url="/new/passage"/>
					<Product name="单句润色" description="提升句子风格和美感。" url="/new/sentense"/>
				</div>
			</section>
		</DefaultLayout>
	);
}
