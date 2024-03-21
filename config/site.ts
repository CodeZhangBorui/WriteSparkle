export type SiteConfig = typeof siteConfig;

export const siteConfig = {
	name: "WriteSparkle",
	description: "It's time to enhance your writing with AI.",
	navItems: [
		{
			label: "主页",
			href: "/",
		},
    {
      label: "文章润色",
      href: "/new/passage",
    },
    {
      label: "句子润色",
      href: "/new/sentense",
    },
    {
      label: "关于",
      href: "/about",
    }
	],
	navMenuItems: [
		// {
		// 	label: "Profile",
		// 	href: "/profile",
		// },
		// {
		// 	label: "Dashboard",
		// 	href: "/dashboard",
		// },
		// {
		// 	label: "Projects",
		// 	href: "/projects",
		// },
		// {
		// 	label: "Team",
		// 	href: "/team",
		// },
		// {
		// 	label: "Calendar",
		// 	href: "/calendar",
		// },
		// {
		// 	label: "Settings",
		// 	href: "/settings",
		// },
		// {
		// 	label: "Help & Feedback",
		// 	href: "/help-feedback",
		// },
		// {
		// 	label: "Logout",
		// 	href: "/logout",
		// },
	],
	links: {
		github: "https://github.com/CodeZhangBorui/WriteSparkle",
	},
};
