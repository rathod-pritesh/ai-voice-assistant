<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { initLoadingAnimation } from "$lib/animations/loadingAnimation";

  let canvas;
  let progress = 0;
  let initialized = false;

  onMount(() => {
    const cleanup = initLoadingAnimation(canvas);

    const interval = setInterval(() => {
      progress += 2;
      if (progress >= 100) {
        clearInterval(interval);
        initialized = true;
        setTimeout(() => goto("/home"), 500);
      }
    }, 30);

    return () => {
      cleanup();
      clearInterval(interval);
    };
  });

  let msg = "Loading...";

  onMount(async () => {
    const res = await fetch("http://127.0.0.1:8000/api/hello");
    const data = await res.json();
    msg = data.message;
  });
</script>

<div
  class="min-h-screen bg-slate-900 flex items-center justify-center overflow-hidden relative"
>

  <canvas bind:this={canvas} class="absolute inset-0 w-full h-full"></canvas>

  <div
    class="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-transparent to-purple-900/20 pointer-events-none"
  ></div>

  <p class="absolute top-4 left-4 text-white text-sm opacity-70">
  {msg}
  </p>

  <div class="relative z-10 flex flex-col items-center gap-8">

    <div class="relative w-48 h-48 md:w-64 md:h-64">

      <div
        class="absolute inset-0 rounded-full border-2 border-cyan-500/30 animate-spin-slow"
      ></div>

      <div
        class="absolute inset-4 rounded-full border-2 border-blue-400/40 animate-spin-reverse"
      ></div>

      <div
        class="absolute inset-8 rounded-full bg-gradient-to-br from-cyan-500/20 to-blue-600/20 animate-pulse-slow flex items-center justify-center"
      >

        <div
          class="w-24 h-24 md:w-32 md:h-32 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center shadow-lg shadow-cyan-500/50"
        >
          <div
            class="w-20 h-20 md:w-28 md:h-28
         rounded-full bg-gradient-to-br from-cyan-500 to-blue-600
         flex items-center justify-center
         shadow-2xl shadow-cyan-500/30
         animate-pulse-slow mx-auto"
          >
            <i
              class="fa-solid fa-robot text-white text-5xl drop-shadow-[0_0_10px_rgba(59,130,246,0.6)]"
            ></i>
          </div>
        </div>
      </div>

      <!-- Progress arc -->
      <svg class="absolute inset-0 w-full h-full -rotate-90">
        <circle
          cx="50%"
          cy="50%"
          r="45%"
          fill="none"
          stroke="url(#gradient)"
          stroke-width="3"
          stroke-dasharray="628"
          stroke-dashoffset={628 - (628 * progress) / 100}
          class="transition-all duration-300"
          stroke-linecap="round"
        />
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#06b6d4;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
          </linearGradient>
        </defs>
      </svg>
    </div>

    <div class="text-center space-y-4">
      <h1
        class="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500"
      >
        Saarthi
      </h1>
      <p class="text-cyan-300/80 text-lg md:text-xl font-light tracking-wide">
        {initialized ? "Initialization Complete" : "Initializing System..."}
      </p>
      <div
        class="flex items-center justify-center gap-2 text-blue-400/60 text-sm"
      >
        <span>{progress}%</span>
        <div class="flex gap-1">
          <div
            class="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce"
            style="animation-delay: 0ms"
          ></div>
          <div
            class="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce"
            style="animation-delay: 150ms"
          ></div>
          <div
            class="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce"
            style="animation-delay: 300ms"
          ></div>
        </div>
      </div>
    </div>
  </div>

  <div
    class="absolute top-8 left-8 w-16 h-16 border-t-2 border-l-2 border-cyan-500/30 z-10"
  ></div>
  <div
    class="absolute top-8 right-8 w-16 h-16 border-t-2 border-r-2 border-cyan-500/30 z-10"
  ></div>
  <div
    class="absolute bottom-8 left-8 w-16 h-16 border-b-2 border-l-2 border-cyan-500/30 z-10"
  ></div>
  <div
    class="absolute bottom-8 right-8 w-16 h-16 border-b-2 border-r-2 border-cyan-500/30 z-10"
  ></div>
</div>

<style>
  @keyframes spin-slow {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  @keyframes spin-reverse {
    from {
      transform: rotate(360deg);
    }
    to {
      transform: rotate(0deg);
    }
  }

  @keyframes pulse-slow {
    0%,
    100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.8;
      transform: scale(1.05);
    }
  }

  .animate-spin-slow {
    animation: spin-slow 3s linear infinite;
  }

  .animate-spin-reverse {
    animation: spin-reverse 4s linear infinite;
  }

  .animate-pulse-slow {
    animation: pulse-slow 2s ease-in-out infinite;
  }
</style>
