<script>
	import { onMount } from "svelte";
	import { Toaster } from "svelte-sonner";
	import { initHomeAnimation } from "$lib/animations/homeAnimation";
	import "../app.css";

	let { children } = $props();
	let canvas;

	onMount(() => {
		const cleanup = initHomeAnimation(canvas);
		return cleanup;
	});
</script>

<Toaster position="top-right" richColors />

<div class="relative min-h-screen bg-[#F5F6F3] text-[#1C1E1D] overflow-x-hidden selection:bg-[#2F7A5F]/20 selection:text-[#2F7A5F]">
	<!-- Global Persistent Particle Background -->
	<canvas bind:this={canvas} class="fixed inset-0 w-full h-full pointer-events-none z-0 opacity-60"></canvas>

	<!-- Subtle Ambient Glow Orbs -->
	<div class="fixed top-1/4 -left-48 w-96 h-96 bg-[#2F7A5F]/10 rounded-full blur-3xl pointer-events-none z-0 animate-pulse"></div>
	<div class="fixed bottom-1/4 -right-48 w-96 h-96 bg-[#A5C882]/15 rounded-full blur-3xl pointer-events-none z-0 animate-pulse" style="animation-delay: 2s"></div>

	<div class="relative z-10 min-h-screen flex flex-col">
		{@render children?.()}
	</div>
</div>
