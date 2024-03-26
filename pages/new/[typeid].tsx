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
import { Button, Textarea } from "@nextui-org/react";
import { ChangeEventHandler, SetStateAction, useState } from "react";
import { useRouter } from "next/router";

export default function IndexPage() {
  const router = useRouter();
  const { typeid } = router.query;

  const [textareaContent, setTextareaContent] = useState("");

  const handleTextareaChange = (e: { target: { value: SetStateAction<string>; }; }) => {
    setTextareaContent(e.target.value);
  };

  const handleButtonClick = () => {
    console.log(textareaContent);
  };

  return (
    <DefaultLayout>
      <section
        className="flex flex-col gap-4 py-8 md:py-10"
        style={{ marginLeft: "18%", marginRight: "18%" }}
      >
        <h1 className={title()}>读后续写润色</h1>
        <Textarea
          label="输入作文"
          variant="bordered"
          placeholder="Enter your writing"
          disableAutosize
          value={textareaContent}
          onChange={handleTextareaChange}
          classNames={{
            base: "w-full",
            input: "resize-y min-h-[200px]",
          }}
        />
        <Button color="primary" className="w-32" onClick={handleButtonClick}>
          提交
        </Button>
      </section>
    </DefaultLayout>
  );
}
