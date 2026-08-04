<script>
  import { onMount, tick } from "svelte";
  import { goto } from "$app/navigation";
  import { fade, scale, slide } from "svelte/transition";
  import { toast } from "svelte-sonner";
  import { 
    Mic, Send, Bot, Volume2, Zap, Lightbulb, 
    LogOut, PanelLeft, Plus, X, SquarePen, Settings,
    User, Mail, Sliders, ShieldCheck, ChevronRight, HelpCircle, Layers
  } from "lucide-svelte";

  let hideFeatures = false;
  let isRecording = false;
  let recognition = null;
  let chatInput;
  let user = null;
  let chats = [];
  let showSidebar = false;
  let showSettingsModal = false;
  let showLogoutModal = false;
  let activeTab = "features";

  // Settings state (UI only)
  let voiceRate = 1.0;
  let voicePitch = 1.0;

  onMount(() => {
    const stored = localStorage.getItem("user");
    if (stored) {
      user = JSON.parse(stored);
    }
  });

  onMount(() => {
    if (typeof window === "undefined") return;

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      console.warn("SpeechRecognition not supported in this browser.");
      return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      console.log("Speech transcript:", text);

      if (text.length === 0) return;

      message = text;
      sendMessage();
    };

    recognition.onend = () => {
      isRecording = false;
    };

    recognition.onerror = (event) => {
      console.error(
        "Speech Recognition error:",
        event.error,
        event.message,
        event
      );
      isRecording = false;
      toast.error("Speech recognition error: " + (event.error || "Try speaking again"));
    };

    console.log("SpeechRecognition engine ready:", recognition);
  });

  function toggleRecording() {
    if (!user) {
      toast.error("Please log in to use voice input.");
      goto("/login");
      return;
    }

    if (!recognition) {
      toast.error("Speech recognition is not supported on this browser.");
      return;
    }

    if (isRecording) {
      recognition.stop();
      isRecording = false;
      console.log("Stopped recording");
    } else {
      try {
        recognition.start();
        isRecording = true;
        hideFeatures = true;
        toast.info("Listening for voice input...");
      } catch (err) {
        console.error("Error starting recognition:", err);
        isRecording = false;
      }
    }
  }

  function speak(text) {
    if (!window.speechSynthesis) {
      console.warn("Speech Synthesis not supported.");
      return;
    }

    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = "en-US";
    utter.pitch = voicePitch;
    utter.rate = voiceRate;
    utter.volume = 1;

    window.speechSynthesis.speak(utter);
  }

  let message = "";

  async function sendMessage() {
    if (!user) {
      toast.error("Please log in to send prompts.");
      goto("/login");
      return;
    }

    const userMsg = message.trim();
    if (!userMsg) return;

    hideFeatures = true;
    chats = [...chats, { sender: user.name || "User", text: userMsg }];

    message = "";
    if (chatInput) chatInput.style.height = "44px";

    try {
      const res = await fetch("http://localhost:8000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userMsg }),
      });

      const data = await res.json();

      chats = [...chats, { sender: "Saarthi", text: data.reply }];

      speak(data.reply);

      await tick();
      const el = document.getElementById("chat-scroll");
      if (el) el.scrollTop = el.scrollHeight;
    } catch (e) {
      console.error("API error:", e);
      toast.error("Unable to get AI response. Please ensure backend server is running.");
    }
  }

  function openLogoutModal() {
    showLogoutModal = true;
  }

  function confirmLogout() {
    if (typeof window !== "undefined") {
      localStorage.removeItem("user");
    }
    user = null;
    chats = [];
    hideFeatures = false;
    showLogoutModal = false;
    showSidebar = false;
    toast.success("Successfully logged out");
  }

  function clearChat() {
    chats = [];
    hideFeatures = false;
    toast.info("Cleared conversation session");
  }

  function usePrompt(promptText) {
    if (!user) {
      goto("/login");
      return;
    }
    message = promptText;
    sendMessage();
  }
</script>

<div class="relative min-h-screen text-[#1C1E1D] flex flex-col justify-between overflow-x-hidden">

  <!-- Sidebar Drawer Backdrop (Mobile) -->
  {#if showSidebar}
    <button
      type="button"
      aria-label="Close navigation drawer"
      transition:fade={{ duration: 200 }}
      on:click={() => (showSidebar = false)}
      on:keydown={(e) => e.key === 'Escape' && (showSidebar = false)}
      class="fixed inset-0 bg-black/40 backdrop-blur-xs z-50 lg:hidden cursor-default border-none p-0 text-left w-full h-full"
    ></button>
  {/if}

  <!-- Sidebar Drawer Navigation (ChatGPT Style) -->
  <aside
    class={`fixed top-0 left-0 bottom-0 w-72 bg-[#202623] border-r border-[#202623] text-white z-50 flex flex-col justify-between transition-transform duration-300 shadow-2xl ${showSidebar ? "translate-x-0" : "-translate-x-full"}`}
  >
    <div class="p-4 space-y-5 flex-1 flex flex-col overflow-y-auto">
      
      <!-- Sidebar Header with Logo -->
      <div class="flex items-center justify-between pb-2 border-b border-white/10">
        <div class="flex items-center gap-3">
          <img src="/images/logo.png" alt="Saarthi Logo" class="w-8 h-8 object-contain rounded-lg bg-white/10 p-0.5" />
          <h2 class="font-extrabold text-white text-base tracking-wide">Saarthi</h2>
        </div>

        <button
          on:click={() => (showSidebar = false)}
          class="p-1.5 text-slate-400 hover:text-white hover:bg-white/10 rounded-lg transition cursor-pointer"
          title="Close sidebar"
        >
          <X class="w-4 h-4" />
        </button>
      </div>

      <!-- New Chat Button -->
      <button
        on:click={() => { if (!user) { goto("/login"); return; } clearChat(); if (window.innerWidth < 1024) showSidebar = false; }}
        class="w-full py-2.5 px-4 rounded-xl bg-[#2F7A5F] hover:bg-[#26664E] text-white text-xs font-semibold shadow-md shadow-[#2F7A5F]/20 transition flex items-center justify-center gap-2 cursor-pointer"
      >
        <Plus class="w-4 h-4" />
        <span>New Chat Session</span>
      </button>

      <!-- Preset Voice Prompts -->
      <div class="space-y-2 flex-1">
        <p class="text-[11px] font-bold uppercase tracking-wider text-[#D9DDD8]/60 px-1">
          Quick Starter Prompts
        </p>

        <div class="space-y-1.5">
          <button
            on:click={() => { usePrompt("What can you help me with today?"); if (window.innerWidth < 1024) showSidebar = false; }}
            class="w-full text-left p-2.5 rounded-xl bg-[#2A322E] hover:bg-[#323C37] border border-white/5 text-xs text-slate-200 transition flex items-center justify-between group cursor-pointer"
          >
            <span class="truncate">What can you help me with?</span>
            <ChevronRight class="w-3.5 h-3.5 text-[#A5C882] group-hover:translate-x-0.5 transition-transform" />
          </button>

          <button
            on:click={() => { usePrompt("Explain quantum computing in simple terms"); if (window.innerWidth < 1024) showSidebar = false; }}
            class="w-full text-left p-2.5 rounded-xl bg-[#2A322E] hover:bg-[#323C37] border border-white/5 text-xs text-slate-200 transition flex items-center justify-between group cursor-pointer"
          >
            <span class="truncate">Explain quantum computing</span>
            <ChevronRight class="w-3.5 h-3.5 text-[#A5C882] group-hover:translate-x-0.5 transition-transform" />
          </button>

          <button
            on:click={() => { usePrompt("Give me a motivational quote for work"); if (window.innerWidth < 1024) showSidebar = false; }}
            class="w-full text-left p-2.5 rounded-xl bg-[#2A322E] hover:bg-[#323C37] border border-white/5 text-xs text-slate-200 transition flex items-center justify-between group cursor-pointer"
          >
            <span class="truncate">Motivational work quote</span>
            <ChevronRight class="w-3.5 h-3.5 text-[#A5C882] group-hover:translate-x-0.5 transition-transform" />
          </button>
        </div>
      </div>
    </div>

    <!-- Sidebar Bottom: Settings & Profile Section -->
    <div class="p-4 border-t border-white/10 space-y-3 bg-[#1A1F1C]">
      
      <!-- Settings Button -->
      <button
        on:click={() => (showSettingsModal = true)}
        class="w-full flex items-center gap-3 p-2.5 rounded-xl bg-[#2A322E]/80 hover:bg-[#323C37] border border-white/5 text-xs font-semibold text-slate-200 hover:text-white transition cursor-pointer"
      >
        <Settings class="w-4 h-4 text-[#A5C882]" />
        <span>Voice & App Settings</span>
      </button>

      <!-- Profile Section -->
      {#if user}
        <div class="p-3 rounded-xl bg-[#202623] border border-white/10 flex items-center justify-between">
          <div class="flex items-center gap-2.5 overflow-hidden">
            {#if user.picture}
              <img src={user.picture} alt={user.name} class="w-8 h-8 rounded-xl object-cover border border-[#2F7A5F]" />
            {:else}
              <div class="w-8 h-8 rounded-xl bg-[#2F7A5F] text-white font-extrabold text-xs flex items-center justify-center flex-shrink-0 shadow-xs">
                {user.name ? user.name.charAt(0).toUpperCase() : "U"}
              </div>
            {/if}
            <div class="overflow-hidden leading-tight">
              <p class="text-xs font-bold text-white truncate">{user.name}</p>
              <p class="text-[10px] text-slate-400 truncate">{user.email || "User Session"}</p>
            </div>
          </div>

          <button
            on:click={openLogoutModal}
            class="p-2 text-slate-400 hover:text-[#C45A4D] hover:bg-white/5 rounded-lg transition cursor-pointer"
            title="Log out"
          >
            <LogOut class="w-4 h-4" />
          </button>
        </div>
      {:else}
        <div class="flex items-center gap-2 pt-1">
          <button
            on:click={() => goto("/login")}
            class="flex-1 py-2 px-3 text-center rounded-xl bg-white/5 hover:bg-white/10 text-xs font-semibold text-slate-200 border border-white/10 transition"
          >
            Log In
          </button>
          <button
            on:click={() => goto("/signup")}
            class="flex-1 py-2 px-3 text-center rounded-xl bg-[#2F7A5F] hover:bg-[#26664E] text-xs font-semibold text-white transition"
          >
            Sign Up
          </button>
        </div>
      {/if}
    </div>
  </aside>

  <!-- Main Content Body -->
  <div class={`flex-1 flex flex-col min-h-screen transition-all duration-300 ${showSidebar ? "lg:pl-72" : "lg:pl-0"}`}>
    
    <!-- Top Navigation Bar (Aligned Left with Center Links) -->
    <header class="sticky top-0 z-40 bg-[#FFFFFF] border-b border-[#D9DDD8] shadow-xs px-2 sm:px-4">
      <div class="w-full flex items-center justify-between py-3">
        
        <!-- Left: Toggle Sidebar, New Session Icon, Logo & Title (Tight Left) -->
        <div class="flex items-center gap-2">
          <!-- Sidebar Toggle -->
          <button
            on:click={() => (showSidebar = !showSidebar)}
            class="p-2 text-[#646B67] hover:text-[#2F7A5F] hover:bg-[#F5F6F3] rounded-xl transition cursor-pointer"
            aria-label="Toggle navigation menu"
            title="Toggle sidebar menu"
          >
            <PanelLeft class="w-5 h-5" />
          </button>

          <!-- New Session Quick Icon -->
          <button
            on:click={() => { if (!user) { goto("/login"); return; } clearChat(); }}
            class="p-2 text-[#646B67] hover:text-[#2F7A5F] hover:bg-[#F5F6F3] rounded-xl transition cursor-pointer"
            aria-label="New chat session"
            title="Start new chat"
          >
            <SquarePen class="w-5 h-5" />
          </button>

          <!-- Logo & Title -->
          <div class="flex items-center gap-2.5 ml-1">
            <img src="/images/logo.png" alt="Saarthi Logo" class="w-8 h-8 object-contain rounded-lg border border-[#D9DDD8] p-0.5" />
            <h1 class="text-base font-extrabold text-[#1C1E1D] leading-tight tracking-tight">
              Saarthi
            </h1>
          </div>
        </div>

        <!-- Center Product Navigation Links -->
        <nav class="hidden md:flex items-center gap-1 bg-[#F5F6F3] p-1 rounded-2xl border border-[#D9DDD8]">
          <button
            on:click={() => (activeTab = "features")}
            class={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition cursor-pointer ${
              activeTab === "features"
                ? "bg-[#FFFFFF] text-[#2F7A5F] shadow-xs"
                : "text-[#646B67] hover:text-[#1C1E1D]"
            }`}
          >
            Features
          </button>

          <button
            on:click={() => (activeTab = "works")}
            class={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition cursor-pointer ${
              activeTab === "works"
                ? "bg-[#FFFFFF] text-[#2F7A5F] shadow-xs"
                : "text-[#646B67] hover:text-[#1C1E1D]"
            }`}
          >
            How it Works
          </button>

          <button
            on:click={() => (activeTab = "capabilities")}
            class={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition cursor-pointer ${
              activeTab === "capabilities"
                ? "bg-[#FFFFFF] text-[#2F7A5F] shadow-xs"
                : "text-[#646B67] hover:text-[#1C1E1D]"
            }`}
          >
            Capabilities
          </button>
        </nav>

        <!-- Right Action Auth Controls -->
        <div class="flex items-center gap-3">
          {#if user}
            <div class="flex items-center gap-2">
              {#if user.picture}
                <img src={user.picture} alt={user.name} class="w-7 h-7 rounded-full object-cover border border-[#2F7A5F]" />
              {:else}
                <div class="w-7 h-7 rounded-full bg-[#2F7A5F] text-white font-extrabold text-xs flex items-center justify-center shadow-xs">
                  {user.name ? user.name.charAt(0).toUpperCase() : "U"}
                </div>
              {/if}
              <span class="text-[#1C1E1D] text-xs font-bold hidden sm:inline">{user.name}</span>
            </div>

            <button
              on:click={openLogoutModal}
              class="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-[#C45A4D] bg-[#C45A4D]/10 border border-[#C45A4D]/30 hover:bg-[#C45A4D] hover:text-white transition duration-300 cursor-pointer"
            >
              Logout
            </button>
          {:else}
            <button
              on:click={() => goto("/login")}
              class="px-4 py-2 text-xs font-semibold text-[#646B67] hover:text-[#1C1E1D] rounded-xl border border-[#D9DDD8] hover:border-[#646B67] bg-[#FFFFFF] transition cursor-pointer"
            >
              Log In
            </button>
            <button
              on:click={() => goto("/signup")}
              class="px-4 py-2 text-xs font-semibold text-white bg-[#2F7A5F] hover:bg-[#26664E] rounded-xl shadow-md shadow-[#2F7A5F]/20 transition cursor-pointer"
            >
              Sign Up
            </button>
          {/if}
        </div>
      </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="flex-1 max-w-4xl w-full mx-auto px-4 py-8 flex flex-col justify-between pb-36">

      {#if user}
        <!-- LOGGED-IN CHAT WORKSPACE -->
        <div id="chat-scroll" class="space-y-6 overflow-y-auto max-h-[55vh] px-1 py-2">
          {#each chats as c}
            {#if c.sender !== "Saarthi"}
              <!-- User Message -->
              <div class="flex justify-end" in:fade={{ duration: 200 }}>
                <div class="max-w-[80%] bg-[#2F7A5F] text-white px-5 py-3.5 rounded-3xl rounded-tr-xs shadow-md">
                  <div class="flex items-center justify-end gap-2 mb-1">
                    <span class="font-semibold text-xs text-[#A5C882]">{c.sender}</span>
                    {#if user && user.picture}
                      <img src={user.picture} alt={c.sender} class="w-5 h-5 rounded-full object-cover border border-[#A5C882]/40" />
                    {:else}
                      <div class="w-5 h-5 rounded-full bg-[#A5C882] text-[#202623] font-extrabold text-[10px] flex items-center justify-center shadow-xs">
                        {c.sender ? c.sender.charAt(0).toUpperCase() : 'U'}
                      </div>
                    {/if}
                  </div>
                  <p class="text-sm leading-relaxed">{c.text}</p>
                </div>
              </div>
            {/if}

            {#if c.sender === "Saarthi"}
              <!-- AI Response with Logo Avatar -->
              <div class="flex justify-start" in:fade={{ duration: 200 }}>
                <div class="max-w-[85%] bg-[#FFFFFF] border border-[#D9DDD8] text-[#1C1E1D] px-5 py-4 rounded-3xl rounded-tl-xs shadow-md">
                  <div class="flex items-center gap-2.5 mb-2">
                    <div class="w-6 h-6 rounded-lg bg-[#F5F6F3] border border-[#D9DDD8] p-0.5 flex items-center justify-center flex-shrink-0">
                      <img src="/images/logo.png" alt="Saarthi Logo" class="w-full h-full object-contain" />
                    </div>
                    <span class="font-bold text-xs text-[#2F7A5F]">Saarthi AI</span>
                  </div>
                  <p class="text-sm leading-relaxed whitespace-pre-line text-[#1C1E1D]">{c.text}</p>
                </div>
              </div>
            {/if}
          {/each}
        </div>

        {#if !hideFeatures && chats.length === 0}
          <div in:scale={{ duration: 300, start: 0.95 }} out:slide={{ duration: 200 }} class="space-y-8 my-auto py-6">
            <div class="text-center space-y-3">
              <h2 class="text-3xl md:text-4xl font-extrabold text-[#1C1E1D] tracking-tight">
                Welcome back, <span class="text-[#2F7A5F]">{user.name}</span>
              </h2>
              <p class="text-[#646B67] max-w-xl mx-auto text-sm md:text-base">
                Tap the microphone below or pick a prompt from the sidebar to begin your hands-free voice session.
              </p>
            </div>
          </div>
        {/if}

      {:else}
        <!-- LOGGED-OUT PRODUCT SHOWCASE LANDING VIEW -->
        <div in:fade={{ duration: 300 }} class="space-y-12 my-auto py-6">
          
          <!-- Hero Section -->
          <div class="text-center space-y-4">
            <h2 class="text-4xl md:text-5xl font-extrabold text-[#1C1E1D] tracking-tight leading-tight">
              Meet <span class="text-[#2F7A5F]">Saarthi</span>, Your Neural Voice Companion
            </h2>
            
            <p class="text-[#646B67] max-w-2xl mx-auto text-base md:text-lg leading-relaxed">
              Experience instant hands-free speech recognition paired with intelligent neural responses. Log in to start chatting live with voice synthesis.
            </p>
          </div>

          <!-- Section Switcher Content -->
          {#if activeTab === "features"}
            <!-- Tab 1: Features -->
            <div in:scale={{ duration: 250, start: 0.98 }} class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              <div class="p-6 rounded-3xl bg-[#FFFFFF] border border-[#D9DDD8] shadow-sm hover:shadow-md transition">
                <div class="w-12 h-12 rounded-2xl bg-[#2F7A5F]/10 border border-[#2F7A5F]/20 flex items-center justify-center text-[#2F7A5F] mb-4">
                  <Mic class="w-6 h-6" />
                </div>
                <h3 class="font-bold text-[#1C1E1D] text-lg">Real-Time Voice Input</h3>
                <p class="text-xs text-[#646B67] mt-2 leading-relaxed">High-precision browser speech recognition translates your spoken queries into instant AI prompts.</p>
              </div>

              <div class="p-6 rounded-3xl bg-[#FFFFFF] border border-[#D9DDD8] shadow-sm hover:shadow-md transition">
                <div class="w-12 h-12 rounded-2xl bg-[#2F7A5F]/10 border border-[#2F7A5F]/20 flex items-center justify-center text-[#2F7A5F] mb-4">
                  <Bot class="w-6 h-6" />
                </div>
                <h3 class="font-bold text-[#1C1E1D] text-lg">Neural Dialogue</h3>
                <p class="text-xs text-[#646B67] mt-2 leading-relaxed">Engage in natural, context-aware conversations powered by state-of-the-art AI language models.</p>
              </div>

              <div class="p-6 rounded-3xl bg-[#FFFFFF] border border-[#D9DDD8] shadow-sm hover:shadow-md transition">
                <div class="w-12 h-12 rounded-2xl bg-[#2F7A5F]/10 border border-[#2F7A5F]/20 flex items-center justify-center text-[#2F7A5F] mb-4">
                  <Volume2 class="w-6 h-6" />
                </div>
                <h3 class="font-bold text-[#1C1E1D] text-lg">Speech Synthesis</h3>
                <p class="text-xs text-[#646B67] mt-2 leading-relaxed">Listen to crisp, natural audio replies spoken back directly through your browser speakers.</p>
              </div>
            </div>
          {:else if activeTab === "works"}
            <!-- Tab 2: How It Works -->
            <div in:scale={{ duration: 250, start: 0.98 }} class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="p-6 rounded-3xl bg-[#FFFFFF] border border-[#D9DDD8] relative">
                <span class="text-4xl font-extrabold text-[#2F7A5F]/20 absolute top-4 right-5">01</span>
                <h3 class="font-bold text-[#1C1E1D] text-lg mb-2">Speak or Type</h3>
                <p class="text-xs text-[#646B67] leading-relaxed">Click the mic button to talk naturally or type your message into the interactive workspace bar.</p>
              </div>

              <div class="p-6 rounded-3xl bg-[#FFFFFF] border border-[#D9DDD8] relative">
                <span class="text-4xl font-extrabold text-[#2F7A5F]/20 absolute top-4 right-5">02</span>
                <h3 class="font-bold text-[#1C1E1D] text-lg mb-2">Neural Processing</h3>
                <p class="text-xs text-[#646B67] leading-relaxed">Saarthi's backend engine parses your input and synthesizes intelligent, accurate responses.</p>
              </div>

              <div class="p-6 rounded-3xl bg-[#FFFFFF] border border-[#D9DDD8] relative">
                <span class="text-4xl font-extrabold text-[#2F7A5F]/20 absolute top-4 right-5">03</span>
                <h3 class="font-bold text-[#1C1E1D] text-lg mb-2">Voice Response</h3>
                <p class="text-xs text-[#646B67] leading-relaxed">Receive instant text responses while speech synthesis reads the answer back to you seamlessly.</p>
              </div>
            </div>
          {:else}
            <!-- Tab 3: Capabilities -->
            <div in:scale={{ duration: 250, start: 0.98 }} class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div class="p-6 rounded-3xl bg-[#FFFFFF] border border-[#D9DDD8] flex items-start gap-4">
                <div class="w-10 h-10 rounded-xl bg-[#2F7A5F]/10 text-[#2F7A5F] flex items-center justify-center flex-shrink-0">
                  <Zap class="w-5 h-5" />
                </div>
                <div>
                  <h3 class="font-bold text-[#1C1E1D] text-base">Ultra Low Latency</h3>
                  <p class="text-xs text-[#646B67] mt-1 leading-relaxed">Engineered for real-time responsiveness so your voice conversations flow without delay.</p>
                </div>
              </div>

              <div class="p-6 rounded-3xl bg-[#FFFFFF] border border-[#D9DDD8] flex items-start gap-4">
                <div class="w-10 h-10 rounded-xl bg-[#2F7A5F]/10 text-[#2F7A5F] flex items-center justify-center flex-shrink-0">
                  <ShieldCheck class="w-5 h-5" />
                </div>
                <div>
                  <h3 class="font-bold text-[#1C1E1D] text-base">Private & Secure</h3>
                  <p class="text-xs text-[#646B67] mt-1 leading-relaxed">Your audio sessions stay private with secure local session handling and token protection.</p>
                </div>
              </div>
            </div>
          {/if}

          <!-- Guest CTA Card -->
          <div class="p-8 rounded-3xl bg-[#202623] text-white text-center space-y-5 shadow-2xl">
            <div class="w-14 h-14 rounded-2xl bg-[#2F7A5F] flex items-center justify-center mx-auto shadow-lg shadow-[#2F7A5F]/30 p-2">
              <img src="/images/logo.png" alt="Saarthi Logo" class="w-full h-full object-contain" />
            </div>

            <div class="space-y-2">
              <h3 class="text-2xl font-extrabold text-white">Ready to start your voice session?</h3>
              <p class="text-slate-300 text-xs md:text-sm max-w-lg mx-auto">
                Sign in to your account or create a free user profile to access hands-free voice controls and neural dialogue.
              </p>
            </div>

            <div class="flex items-center justify-center gap-3 pt-2">
              <button
                on:click={() => goto("/login")}
                class="px-6 py-2.5 rounded-xl bg-[#2F7A5F] hover:bg-[#26664E] text-white text-xs font-bold shadow-md shadow-[#2F7A5F]/30 transition cursor-pointer"
              >
                Log In to Start
              </button>
              <button
                on:click={() => goto("/signup")}
                class="px-6 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-white text-xs font-bold transition cursor-pointer"
              >
                Create Account
              </button>
            </div>
          </div>

        </div>
      {/if}

    </main>

    <!-- Bottom Floating Input Bar (ONLY for Logged-In Users) -->
    {#if user}
      <div class={`fixed bottom-0 left-0 right-0 pb-6 pt-3 px-4 z-40 bg-gradient-to-t from-[#F5F6F3] via-[#F5F6F3]/90 to-transparent pointer-events-none transition-all duration-300 ${showSidebar ? "lg:pl-72" : "lg:pl-0"}`}>
        <div class="max-w-3xl mx-auto pointer-events-auto">
          
          <form on:submit|preventDefault class="relative">
            <div class="relative flex items-end gap-3 bg-[#FFFFFF] border border-[#D9DDD8] rounded-2xl p-2.5 shadow-xl shadow-slate-200/60 hover:border-[#2F7A5F]/40 transition-all duration-300">
              
              <!-- Textarea Input -->
              <textarea
                bind:value={message}
                bind:this={chatInput}
                rows="1"
                placeholder="Ask Saarthi anything or tap mic..."
                class="flex-1 bg-transparent text-[#1C1E1D] placeholder-[#646B67] outline-none resize-none min-h-[44px] max-h-32 py-2.5 px-3 text-sm"
                on:focus={() => (hideFeatures = true)}
                on:input={(e) => {
                  e.target.style.height = "auto";
                  e.target.style.height = Math.min(e.target.scrollHeight, 128) + "px";
                }}
                on:keydown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                  }
                }}
              ></textarea>

              <!-- Mic Voice Record Button -->
              <button
                type="button"
                aria-label="Toggle voice input"
                on:click={toggleRecording}
                class={`p-3 rounded-xl transition-all duration-300 cursor-pointer ${
                  isRecording
                    ? "bg-[#C45A4D]/15 text-[#C45A4D] border border-[#C45A4D]/40 animate-pulse"
                    : "bg-[#F5F6F3] text-[#646B67] hover:text-[#2F7A5F] hover:bg-[#F0F2ED]"
                }`}
                title={isRecording ? "Stop listening" : "Start voice input"}
              >
                <Mic class="w-5 h-5" />
              </button>

              <!-- Send Button -->
              <button
                type="button"
                on:click={sendMessage}
                aria-label="Send message"
                class="p-3 bg-[#2F7A5F] hover:bg-[#26664E] rounded-xl shadow-md shadow-[#2F7A5F]/20 transition duration-300 text-white cursor-pointer flex-shrink-0"
              >
                <Send class="w-5 h-5" />
              </button>
            </div>
          </form>

          <!-- Listening Modal Overlay -->
          {#if isRecording}
            <div class="fixed inset-0 flex flex-col items-center justify-center bg-black/50 backdrop-blur-xs z-50 animate-fadeIn p-4">
              <div class="bg-[#FFFFFF] p-8 rounded-3xl border border-[#D9DDD8] shadow-2xl flex flex-col items-center max-w-sm w-full text-center">
                <div class="relative w-28 h-28 flex items-center justify-center">
                  
                  <!-- Expanding Aura Pulse -->
                  <div class="absolute inset-0 rounded-full bg-[#2F7A5F]/20 record-pulse"></div>
                  <div class="absolute inset-3 rounded-full bg-[#A5C882]/30 record-pulse" style="animation-delay: 0.3s"></div>

                  <div class="w-16 h-16 rounded-full bg-[#2F7A5F] flex items-center justify-center shadow-lg shadow-[#2F7A5F]/30">
                    <Mic class="w-8 h-8 text-white animate-pulse" />
                  </div>
                </div>

                <!-- Frequency Waveform Graphic -->
                <div class="flex items-center gap-1.5 my-4">
                  <span class="w-1.5 h-6 bg-[#2F7A5F] rounded-full animate-bounce"></span>
                  <span class="w-1.5 h-10 bg-[#A5C882] rounded-full animate-bounce" style="animation-delay: 150ms"></span>
                  <span class="w-1.5 h-12 bg-[#2F7A5F] rounded-full animate-bounce" style="animation-delay: 300ms"></span>
                  <span class="w-1.5 h-8 bg-[#3E8B5A] rounded-full animate-bounce" style="animation-delay: 450ms"></span>
                  <span class="w-1.5 h-5 bg-[#2F7A5F] rounded-full animate-bounce" style="animation-delay: 200ms"></span>
                </div>

                <p class="text-[#1C1E1D] font-bold text-lg tracking-wide">
                  Saarthi is listening...
                </p>
                <p class="text-[#646B67] text-xs mt-1">Speak clearly into your microphone</p>

                <button
                  on:click={toggleRecording}
                  class="mt-5 px-5 py-2 rounded-xl bg-[#F5F6F3] text-[#1C1E1D] hover:bg-[#EAECE6] border border-[#D9DDD8] text-xs font-semibold cursor-pointer"
                >
                  Cancel Listening
                </button>
              </div>
            </div>
          {/if}

        </div>
      </div>
    {/if}

  </div>
</div>

<!-- Settings Modal (UI Only) -->
{#if showSettingsModal}
  <div class="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-xs z-50 animate-fadeIn p-4">
    <div class="bg-[#FFFFFF] p-6 rounded-3xl border border-[#D9DDD8] shadow-2xl max-w-md w-full space-y-6 text-[#1C1E1D]">
      
      <div class="flex items-center justify-between border-b border-[#D9DDD8] pb-3">
        <div class="flex items-center gap-2.5">
          <Settings class="w-5 h-5 text-[#2F7A5F]" />
          <h3 class="font-extrabold text-base text-[#1C1E1D]">Voice & App Settings</h3>
        </div>
        <button
          on:click={() => (showSettingsModal = false)}
          class="p-1.5 text-[#646B67] hover:text-[#1C1E1D] hover:bg-[#F5F6F3] rounded-lg transition cursor-pointer"
        >
          <X class="w-4 h-4" />
        </button>
      </div>

      <div class="space-y-4 text-xs">
        <!-- Voice Speed Slider -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <label for="voice-speed" class="font-bold text-[#1C1E1D]">Speech Rate / Speed</label>
            <span class="font-mono text-[#2F7A5F] font-bold">{voiceRate.toFixed(1)}x</span>
          </div>
          <input
            id="voice-speed"
            type="range"
            min="0.5"
            max="2.0"
            step="0.1"
            bind:value={voiceRate}
            class="w-full accent-[#2F7A5F] cursor-pointer"
          />
        </div>

        <!-- Voice Pitch Slider -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <label for="voice-pitch" class="font-bold text-[#1C1E1D]">Speech Pitch</label>
            <span class="font-mono text-[#2F7A5F] font-bold">{voicePitch.toFixed(1)}</span>
          </div>
          <input
            id="voice-pitch"
            type="range"
            min="0.5"
            max="2.0"
            step="0.1"
            bind:value={voicePitch}
            class="w-full accent-[#2F7A5F] cursor-pointer"
          />
        </div>

        <!-- Theme info -->
        <div class="p-3 rounded-2xl bg-[#F5F6F3] border border-[#D9DDD8] flex items-center justify-between">
          <span class="font-semibold text-[#646B67]">Active Design System</span>
          <span class="px-2.5 py-1 rounded-full bg-[#2F7A5F]/10 text-[#2F7A5F] font-bold text-[11px]">Sage & Forest</span>
        </div>
      </div>

      <div class="pt-2">
        <button
          on:click={() => (showSettingsModal = false)}
          class="w-full py-2.5 rounded-xl bg-[#2F7A5F] hover:bg-[#26664E] text-white font-semibold text-xs transition shadow-md shadow-[#2F7A5F]/20 cursor-pointer"
        >
          Save & Apply Settings
        </button>
      </div>

    </div>
  </div>
{/if}

<!-- Logout Confirmation Modal (Custom UI Modal) -->
{#if showLogoutModal}
  <div class="fixed inset-0 flex items-center justify-center bg-black/50 backdrop-blur-xs z-50 animate-fadeIn p-4">
    <div class="bg-[#FFFFFF] p-6 rounded-3xl border border-[#D9DDD8] shadow-2xl max-w-sm w-full text-center space-y-5 text-[#1C1E1D]">
      
      <div class="w-12 h-12 rounded-2xl bg-[#C45A4D]/10 text-[#C45A4D] flex items-center justify-center mx-auto border border-[#C45A4D]/20">
        <LogOut class="w-6 h-6" />
      </div>

      <div class="space-y-1.5">
        <h3 class="font-extrabold text-lg text-[#1C1E1D]">Confirm Logout</h3>
        <p class="text-xs text-[#646B67] leading-relaxed">
          Are you sure you want to log out of your session? Your current chat view will be cleared.
        </p>
      </div>

      <div class="flex items-center gap-3 pt-2">
        <button
          on:click={() => (showLogoutModal = false)}
          class="flex-1 py-2.5 rounded-xl bg-[#F5F6F3] hover:bg-[#EAECE6] border border-[#D9DDD8] text-[#1C1E1D] text-xs font-semibold transition cursor-pointer"
        >
          Cancel
        </button>
        <button
          on:click={confirmLogout}
          class="flex-1 py-2.5 rounded-xl bg-[#C45A4D] hover:bg-[#A8483B] text-white text-xs font-semibold transition shadow-md shadow-[#C45A4D]/20 cursor-pointer"
        >
          Yes, Logout
        </button>
      </div>

    </div>
  </div>
{/if}

<style>
  @keyframes pulse-record {
    0% {
      transform: scale(0.95);
      opacity: 0.8;
    }
    50% {
      transform: scale(1.4);
      opacity: 0.2;
    }
    100% {
      transform: scale(0.95);
      opacity: 0.8;
    }
  }

  .record-pulse {
    animation: pulse-record 2s infinite ease-in-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .animate-fadeIn {
    animation: fadeIn 0.25s ease-out forwards;
  }
</style>
