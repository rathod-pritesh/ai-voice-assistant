<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { Radio, ShieldCheck, Cpu } from "lucide-svelte";

  let progress = 0;
  let initialized = false;
  let msg = "Connecting to Saarthi Core...";

  onMount(() => {
    const interval = setInterval(() => {
      progress += 2;
      if (progress >= 100) {
        clearInterval(interval);
        initialized = true;
        setTimeout(() => goto("/home"), 400);
      }
    }, 30);

    return () => {
      clearInterval(interval);
    };
  });

  onMount(async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/hello");
      const data = await res.json();
      if (data && data.message) {
        msg = data.message;
      }
    } catch (e) {
      console.warn("Backend connect info fallback", e);
    }
  });
</script>

<div class="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden">
  
  <!-- Main Loader Core -->
  <div class="relative z-10 flex flex-col items-center gap-10 max-w-md w-full text-center">
    
    <!-- Audio Aura & Pulse Orb -->
    <div class="relative w-56 h-56 flex items-center justify-center">
      
      <!-- Outer Pulsing Rings -->
      <div class="absolute inset-0 rounded-full border border-[#2F7A5F]/20 animate-ping opacity-30"></div>
      <div class="absolute inset-4 rounded-full border border-[#2F7A5F]/30 animate-pulse"></div>
      <div class="absolute inset-8 rounded-full border border-[#A5C882]/40"></div>

      <!-- Core Visualizer Card Box with Logo -->
      <div class="relative w-32 h-32 rounded-3xl bg-[#FFFFFF] border-2 border-[#D9DDD8] p-2 shadow-2xl shadow-[#2F7A5F]/20 flex items-center justify-center">
        <div class="w-full h-full rounded-2xl bg-[#F5F6F3] flex items-center justify-center p-3 relative overflow-hidden border border-[#2F7A5F]/20">
          <img src="/images/logo.png" alt="Saarthi Logo" class="w-16 h-16 object-contain animate-pulse" />
          <span class="absolute top-2 right-2 flex h-3 w-3">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#A5C882] opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-[#3E8B5A]"></span>
          </span>
        </div>
      </div>

      <!-- Circular SVG Progress Ring -->
      <svg class="absolute inset-0 w-full h-full -rotate-90">
        <circle
          cx="50%"
          cy="50%"
          r="44%"
          fill="none"
          stroke="#D9DDD8"
          stroke-width="3"
        />
        <circle
          cx="50%"
          cy="50%"
          r="44%"
          fill="none"
          stroke="url(#sageGradient)"
          stroke-width="4"
          stroke-dasharray="680"
          stroke-dashoffset={680 - (680 * progress) / 100}
          class="transition-all duration-150 ease-out"
          stroke-linecap="round"
        />
        <defs>
          <linearGradient id="sageGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#2F7A5F;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#A5C882;stop-opacity:1" />
          </linearGradient>
        </defs>
      </svg>
    </div>

    <!-- Product Branding -->
    <div class="space-y-3">
      <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-[#1C1E1D]">
        Saarthi <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#2F7A5F] to-[#A5C882]">Voice</span>
      </h1>

      <p class="text-[#646B67] text-sm font-medium">
        {initialized ? "Neural System Ready" : "Initializing Voice Engines..."}
      </p>

      <!-- Status Indicator Pill -->
      <div class="inline-flex items-center gap-3 px-4 py-2 rounded-xl bg-[#FFFFFF] border border-[#D9DDD8] text-xs text-[#1C1E1D] shadow-sm">
        <div class="flex items-center gap-1.5">
          <Cpu class="w-3.5 h-3.5 text-[#2F7A5F]" />
          <span>{msg}</span>
        </div>
        <span class="text-[#D9DDD8]">|</span>
        <div class="font-mono text-[#2F7A5F] font-bold">{progress}%</div>
      </div>
    </div>
  </div>

  <!-- Micro Corner Frame Accents -->
  <div class="absolute top-6 left-6 w-8 h-8 border-t border-l border-[#2F7A5F]/40"></div>
  <div class="absolute top-6 right-6 w-8 h-8 border-t border-r border-[#2F7A5F]/40"></div>
  <div class="absolute bottom-6 left-6 w-8 h-8 border-b border-l border-[#2F7A5F]/40"></div>
  <div class="absolute bottom-6 right-6 w-8 h-8 border-b border-r border-[#2F7A5F]/40"></div>
</div>
