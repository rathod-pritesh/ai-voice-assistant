<script>
  import { Eye, EyeOff } from 'lucide-svelte'; 
  import { onMount } from 'svelte';
  import { initHomeAnimation } from '$lib/animations/homeAnimation';
  import { goto } from '$app/navigation';

  let canvas;
  let email = '';
  let password = '';
  let showPassword = false;
  let error = "";

  async function handleLogin() {
    error = "";

    if (!email || !password) {
      error = "Email and Password required.";
      return;
    }

    const res = await fetch("http://localhost:8000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      // Save user session
      localStorage.setItem("user", JSON.stringify({
        name: data.name,
        email: data.email
      }));

      goto("/home");
    }else {
      alert(data.detail);
    }

    goto("/home");
  }

  onMount( () => {
    const cleanup = initHomeAnimation(canvas);
    return cleanup;
  })
</script>

<div class="min-h-screen flex items-center justify-center p-4 bg-black"
>
  <canvas bind:this={canvas} class="fixed inset-0 w-full h-full pointer-events-none"></canvas>

  <div class="w-full max-w-md bg-white p-8 rounded-xl shadow-2xl">
    <h2 class="text-3xl font-bold text-center text-gray-700 mb-8">
      Login to Your Account
    </h2>

    {#if error}
      <p
        class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
        role="alert"
      >
        <strong class="font-bold">Error!</strong>
        <span class="block sm:inline">{error}</span>
      </p>
    {/if}

    <form on:submit|preventDefault={handleLogin} class="space-y-6">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
        <input
          type="email"
          id="email"
          bind:value={email}
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-purple-500 focus:border-purple-500 text-gray-800"
          placeholder="you@example.com"
        />
      </div>

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
        <div class="relative">
          <input
            type={showPassword ? 'text' : 'password'}
            id="password"
            bind:value={password}
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-purple-500 focus:border-purple-500 text-gray-800 pr-10"
            placeholder="••••••"
          />
          <button
            type="button"
            on:click={() => (showPassword = !showPassword)}
            class="absolute inset-y-0 right-0 pr-3 text-gray-600"
          >
            {#if showPassword}
              <EyeOff class="h-5 w-5" />
            {:else}
              <Eye class="h-5 w-5" />
            {/if}
          </button>
        </div>
      </div>

      <p><a href="/forgot-password" class="font-medium text-fg-brand hover:underline">Forgot Password?</a></p>

      <p>Don't have account?
        <a href="/signup" class="font-medium text-fg-brand hover:underline">Sign Up</a>
      </p>

      <button
        type="submit"
        class="w-full py-2 px-4 rounded-lg text-white bg-purple-600 hover:bg-purple-700 transition cursor-pointer"
      >
        Log In
      </button>
    </form>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
  }
</style>