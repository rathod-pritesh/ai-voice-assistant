<script>
  import { onMount, tick } from "svelte";
  import { initHomeAnimation } from "$lib/animations/homeAnimation";
  import { goto } from "$app/navigation";
  import { fade, scale } from "svelte/transition";

  let canvas;
  let hideFeatures = false;
  let isRecording = false;
  let recognition = null;
  let transcribedText = "";
  let chatInput;
  let user = null;
  let chats = [];

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
      console.warn("SpeechRecognition not supported.");
      return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      console.log("Speech:", text);

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
    };

    console.log("SpeechRecognition ready:", recognition);

    // Initialize the background animation
    const cleanup = initHomeAnimation(canvas);
    return cleanup;
  });

  // Toggles the recording state and starts/stops the speech recognition.
  function toggleRecording() {
    if (!recognition) {
      console.warn("Speech recognition object not available.");
      return;
    }

    if (isRecording) {
      recognition.stop();
      isRecording = false;
      console.log("stopped reocording");
    }

    try {
      recognition.start();
      isRecording = true;
      console.log("Started recording...");
    } catch (err) {
      console.error("Error starting recognition:", err);
      isRecording = false;
    }
  }

  function speak(text) {
    if (!window.speechSynthesis) {
      console.warn("Speech Synthesis not supported.");
      return;
    }

    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = "en-US";
    utter.pitch = 1;
    utter.rate = 1;
    utter.volume = 1;

    window.speechSynthesis.speak(utter);
  }

  let message = "";
  let reply = "";

  async function sendMessage() {
    const userMsg = message.trim();
    if (!userMsg) return;

    chats = [...chats, { sender: user ? user.name : "Guest", text: userMsg }];

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

      // Auto scroll
      await tick();
      const el = document.getElementById("chat-scroll");
      if (el) el.scrollTop = el.scrollHeight;
    } catch (e) {
      console.error("API error:", e);
    }
  }

  function logout() {
    if (typeof window !== "undefined") {
      localStorage.removeItem("user");
    }

    alert("Are you sure you want to logout?");
    user = null;
    goto("/home");
  }
</script>

<div
  class="min-h-screen bg-black text-white relative overflow-hidden flex flex-col"
>
  <!-- Background Canvas -->
  <canvas bind:this={canvas} class="fixed inset-0 w-full h-full"></canvas>

  <div class="relative z-10">
    <header
      class="border-b border-slate-700/50 backdrop-blur-md bg-slate-900/30 sticky top-0 z-50"
    >
      <div
        class="container mx-auto px-4 py-4 flex items-center justify-between"
      >
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div
            class="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600
            flex items-center justify-center shadow-lg shadow-cyan-500/30"
          >
            <i
              class="fa-solid fa-robot text-white text-xl
              drop-shadow-[0_0_6px_rgba(59,130,246,0.6)] cursor-pointer"
            ></i>
          </div>

          <div>
            <h1
              class="text-xl font-bold text-transparent bg-clip-text
              bg-gradient-to-r from-cyan-400 to-blue-500 cursor-pointer"
            >
              Saarthi
            </h1>
            <p class="text-xs text-slate-400">
              Your Intelligent Voice Companion
            </p>
          </div>
        </div>

        <!-- Buttons -->
        <div class="flex items-center gap-3">
          {#if user}
            <span class="text-slate-300 text-sm hidden sm:inline"
              >Hi, {user.name}</span
            >
            <button
              on:click={logout}
              class="px-4 py-2 rounded-lg font-medium text-red-400 border border-red-500/50
            hover:bg-red-500 hover:text-white hover:border-red-500
              transition-all duration-300 cursor-pointer">Logout</button
            >
          {:else}
            <button
              out:fade={{ duration: 200 }}
              on:click={() => goto("/login")}
              class="px-4 py-2 text-cyan-400 hover:text-cyan-300 border
            border-cyan-500/50 rounded-lg font-medium hover:border-cyan-400
              transition-all duration-300 text-sm md:text-base cursor-pointer"
            >
              Login
            </button>

            <button
              out:fade={{ duration: 200 }}
              on:click={() => goto("/signup")}
              class="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-600
              rounded-lg font-medium hover:shadow-lg hover:shadow-purple-500/30
              transition-all duration-300 text-sm md:text-base text-white cursor-pointer"
            >
              Sign Up
            </button>
          {/if}
        </div>
      </div>
    </header>

    <main class="container mx-auto px-4 py-16 flex-1 overflow-y-auto pb-40">
      <!-- chat area -->
      <div
        id="chat-scroll"
        class="space-y-6 max-h-[60vh] overflow-y-auto px-2 py-4"
      >
        {#each chats as c}
          <!-- user message -->
          {#if c.sender !== "Saarthi"}
            <div class="flex justify-end">
              <div
                class="max-w-[75%] bg-blue-600/80 text-white px-4 py-3 rounded-2xl shadow-lg"
              >
                <p class="font-semibold text-sm mb-1">{c.sender}</p>
                <p class="text-sm">{c.text}</p>
              </div>
            </div>
          {/if}

          <!-- ai message -->
          {#if c.sender === "Saarthi"}
            <div class="flex justify-start">
              <div
                class="max-w-[75%] bg-slate-800/70 text-slate-200 px-4 py-3 rounded-2xl border border-slate-700 shadow"
              >
                <p class="font-semibold text-cyan-400 text-sm mb-1">Saarthi</p>
                <p class="text-sm">{c.text}</p>
              </div>
            </div>
          {/if}
        {/each}
      </div>

      {#if !hideFeatures}
        <div
          in:scale={{ duration: 300, start: 0.9, opacity: 0 }}
          out:scale={{ duration: 250, start: 1, end: 0.9, opacity: 0 }}
          class="text-center mb-12"
        >
          <h2
            class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500"
          >
            Experience the Difference
          </h2>
          <p class="text-slate-400 mt-3 text-lg">
            Unlock a new level of assistance with Saarthi—your intuitive,
            voice-activated partner for success.
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Feature 1 -->
          <div
            class="p-6 bg-slate-800/40 border border-slate-700/40 rounded-2xl backdrop-blur-md
                hover:border-cyan-500/40 hover:shadow-lg hover:shadow-cyan-500/20
                transition-all duration-300 cursor-pointer"
          >
            <i class="fa-solid fa-microphone text-3xl text-cyan-400"></i>
            <h3 class="text-xl font-semibold mt-4 text-white">
              Voice Commands
            </h3>
            <p class="text-slate-400 mt-2">
              Control apps, ask questions, and execute tasks hands-free.
            </p>
          </div>

          <!-- Feature 2 -->
          <div
            class="p-6 bg-slate-800/40 border border-slate-700/40 rounded-2xl backdrop-blur-md
                hover:border-purple-500/40 hover:shadow-lg hover:shadow-purple-500/20
                transition-all duration-300 cursor-pointer"
          >
            <i class="fa-solid fa-robot text-3xl text-purple-400"></i>
            <h3 class="text-xl font-semibold mt-4 text-white">
              AI Conversation
            </h3>
            <p class="text-slate-400 mt-2">
              Chat naturally with an AI that understands and responds smartly.
            </p>
          </div>

          <!-- Feature 3 -->
          <div
            class="p-6 bg-slate-800/40 border border-slate-700/40 rounded-2xl backdrop-blur-md
                hover:border-blue-500/40 hover:shadow-lg hover:shadow-blue-500/20
                transition-all duration-300 cursor-pointer"
          >
            <i class="fa-solid fa-volume-high text-3xl text-blue-400"></i>
            <h3 class="text-xl font-semibold mt-4 text-white">
              Speech to Text
            </h3>
            <p class="text-slate-400 mt-2">
              Convert spoken words into accurate text for fast processing.
            </p>
          </div>

          <!-- Feature 4 -->
          <div
            class="p-6 bg-slate-800/40 border border-slate-700/40 rounded-2xl backdrop-blur-md
                hover:border-emerald-500/40 hover:shadow-lg hover:shadow-emerald-500/20
                transition-all duration-300 cursor-pointer"
          >
            <i class="fa-solid fa-play text-3xl text-emerald-400"></i>
            <h3 class="text-xl font-semibold mt-4 text-white">
              Text to Speech
            </h3>
            <p class="text-slate-400 mt-2">
              Saarthi can speak responses out loud with natural clarity.
            </p>
          </div>

          <!-- Feature 5 -->
          <div
            class="p-6 bg-slate-800/40 border border-slate-700/40 rounded-2xl backdrop-blur-md
                hover:border-pink-500/40 hover:shadow-lg hover:shadow-pink-500/20
                transition-all duration-300 cursor-pointer"
          >
            <i class="fa-solid fa-lightbulb text-3xl text-pink-400"></i>
            <h3 class="text-xl font-semibold mt-4 text-white">
              Smart Recommendations
            </h3>
            <p class="text-slate-400 mt-2">
              Get personalized suggestions, reminders, and insights instantly.
            </p>
          </div>

          <!-- Feature 6 -->
          <div
            class="p-6 bg-slate-800/40 border border-slate-700/40 rounded-2xl backdrop-blur-md
                hover:border-yellow-500/40 hover:shadow-lg hover:shadow-yellow-500/20
                transition-all duration-300 cursor-pointer"
          >
            <i class="fa-solid fa-gears text-3xl text-yellow-400"></i>
            <h3 class="text-xl font-semibold mt-4 text-white">
              Task Automation
            </h3>
            <p class="text-slate-400 mt-2">
              Automate workflows, open apps, process data, and more.
            </p>
          </div>
        </div>
      {/if}
    </main>

    <div class="fixed bottom-0 inset-x-0 pb-6 z-40">
      <div class="container mx-auto px-4 py-10 max-w-3xl">
        <form class="relative" on:submit|preventDefault>
          <div
            class="relative flex items-end gap-3 bg-slate-800/50 backdrop-blur-md border border-slate-700/40 rounded-2xl p-3 shadow-xl hover:border-cyan-500/40 transition-all duration-300"
          >
            <!-- input -->
            <textarea
              bind:value={message}
              bind:this={chatInput}
              class="flex-1 bg-transparent text-white placeholder-slate-500 outline-none resize-none min-h-[44px] max-h-32 py-3 px-3 text-sm md:text-base"
              placeholder="Ask Saarthi anything..."
              rows="1"
              on:focus={() => (hideFeatures = true)}
              on:input={(e) => {
                e.target.style.height = "auto";
                e.target.style.height =
                  Math.min(e.target.scrollHeight, 128) + "px";
              }}
              on:keydown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage();
                }
              }}
            ></textarea>

            <!-- mic -->
            <button
              type="button"
              aria-label="Voice input"
              on:click={toggleRecording}
              class={`p-3 rounded-xl transition-all duration-300 cursor-pointer ${isRecording ? "text-red-500 animate-pulse" : "text-slate-300 hover:text-cyan-400"}
            `}
            >
              <i class="fa-solid fa-microphone text-lg"></i>
            </button>

            <!-- send -->
            <button
              type="button"
              on:click={sendMessage}
              aria-label="Send message"
              class="p-3 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl
               hover:shadow-lg hover:shadow-cyan-500/30 transition-all
               duration-300 flex-shrink-0 text-white cursor-pointer"
            >
              <i
                class="fa-solid fa-paper-plane text-lg"
                style="transform: rotate(45deg); padding-left: 1px; margin-right: 2px;"
              ></i>
            </button>
          </div>
        </form>

        {#if isRecording}
          <div
            class="fixed inset-0 flex flex-col items-center justify-center bg-black/40 backdrop-blur-sm z-50 animate-fadeIn"
          >
            
            <div class="relative w-28 h-28 flex items-center justify-center">
              <div
                class="absolute inset-0 rounded-full bg-red-500/30 record-pulse"
              ></div>

              <div
                class="w-16 h-16 rounded-full bg-red-600 flex items-center justify-center shadow-xl"
              >
                <i class="fa-solid fa-microphone text-white text-3xl"></i>
              </div>
            </div>

            <p class="text-red-300 text-lg mt-3 tracking-wide animate-pulse">
              Listening...
            </p>
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  @keyframes pulse-record {
    0% {
      transform: scale(1);
      opacity: 0.8;
    }
    50% {
      transform: scale(1.4);
      opacity: 0.3;
    }
    100% {
      transform: scale(1);
      opacity: 0.8;
    }
  }

  .record-pulse {
    animation: pulse-record 1.3s infinite ease-in-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .animate-fadeIn {
    animation: fadeIn 0.3s ease-out forwards;
  }

  @keyframes pulse-slow {
    0%,
    100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.85;
      transform: scale(1.05);
    }
  }
</style>
