<script>
  import { initHomeAnimation } from "$lib/animations/homeAnimation";
  import { onMount } from "svelte";

  let canvas;
  let email = "";

  onMount(() => {
    const cleanup = initHomeAnimation(canvas);
    return cleanup;
  });

  async function handleForgotPassword() {
    if (!email.trim()) {
      alert("Please enter an email");
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/api/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail);
        return;
      }

      // SUCCESS
      sessionStorage.setItem("reset_email", email.trim());
      window.location.href = "/verify-otp";

    } catch (err) {
      console.error("API error", err);
      alert("Something went wrong. Check backend.");
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center p-4 bg-black relative overflow-hidden">
  <!-- Background Animation -->
  <canvas bind:this={canvas} class="fixed inset-0 w-full h-full pointer-events-none"></canvas>

  <!-- Form Box -->
  <div class="w-full max-w-md bg-white p-8 rounded-xl shadow-2xl relative z-10">
    <h2 class="text-3xl font-bold text-center text-gray-700 mb-8">
      Enter your email address
    </h2>

    <form on:submit|preventDefault={handleForgotPassword} class="space-y-6">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
          Email Address
        </label>
        <input
          type="email"
          id="email"
          bind:value={email}
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg 
                 focus:ring-purple-500 focus:border-purple-500 text-gray-800"
          placeholder="you@example.com"
        />
      </div>

      <button
        type="submit"
        class="w-full py-2 px-4 rounded-lg text-white bg-purple-600 
               hover:bg-purple-700 transition cursor-pointer"
      >
        Send OTP
      </button>
    </form>
  </div>
</div>
