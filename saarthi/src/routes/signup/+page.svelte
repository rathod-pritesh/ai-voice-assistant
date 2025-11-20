<script>
  import { Eye, EyeOff } from "lucide-svelte";
  import { onMount } from "svelte";
  import { initHomeAnimation } from "$lib/animations/homeAnimation";
  import { goto } from "$app/navigation";

  let canvas;

  let name = "";
  let email = "";
  let password = "";
  let confirmPassword = "";
  let showPassword = false;
  let showConfirmPassword = false;

  let error = "";
  let success = "";

  $: passwordsMatch = password === confirmPassword;

  async function handleSignup() {
    error = "";
    success = "";

    if (!name || !email || !password || !confirmPassword) {
      error = "All fields are required";
      return;
    }

    if (password.length < 6) {
      error = "Password must be at leasr 6 characters";
      return;
    }

    if (password != confirmPassword) {
      error = "Passwords do not match";
      return;
    }

    const res = await fetch("http://localhost:8000/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      error = data.detail;
      return;
    }

    success = "Signup successful!";
    setTimeout(() => goto("/login"), 1200);
  }

  onMount(() => {
    const cleanup = initHomeAnimation(canvas);
    return cleanup;
  });
</script>

<div
  class="min-h-screen flex items-center justify-center p-4 bg-black"
>
  <canvas
    bind:this={canvas}
    class="fixed inset-0 w-full h-full pointer-events-none"
  ></canvas>

  <div class="w-full max-w-lg bg-white p-8 rounded-xl shadow-2xl">
    <h2 class="text-3xl font-bold text-center text-gray-700 mb-8">
      Create Your Account
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

    {#if success}
      <p
        class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative"
        role="alert"
      >
        <strong class="font-bold">Success!</strong>
        <span class="block sm:inline">{success}</span>
      </p>
    {/if}

    <form on:submit|preventDefault={handleSignup} class="space-y-6">
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 mb-1"
          >Full Name</label
        >
        <input
          type="text"
          id="name"
          bind:value={name}
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-purple-500 focus:border-purple-500 text-gray-800"
          placeholder="John Doe"
        />
      </div>

      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1"
          >Email Address</label
        >
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
        <label
          for="password"
          class="block text-sm font-medium text-gray-700 mb-1">Password</label
        >
        <div class="relative">
          <input
            type={showPassword ? "text" : "password"}
            id="password"
            bind:value={password}
            required
            minlength="6"
            class="w-full px-4 py-2 border {passwordsMatch || password === ''
              ? 'border-gray-300'
              : 'border-red-500'} rounded-lg focus:ring-purple-500 focus:border-purple-500 text-gray-800 pr-10"
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

      <div>
        <label
          for="confirm-password"
          class="block text-sm font-medium text-gray-700 mb-1"
          >Confirm Password</label
        >
        <div class="relative">
          <input
            type={showConfirmPassword ? "text" : "password"}
            id="confirm-password"
            bind:value={confirmPassword}
            required
            class="w-full px-4 py-2 border rounded-lg focus:ring-purple-500 focus:border-purple-500 text-gray-800 pr-10 
            {confirmPassword && !passwordsMatch ? 'border-red-500' : 'border-gray-300'}"
            placeholder="••••••"
          />
          <button
            type="button"
            on:click={() => (showConfirmPassword = !showConfirmPassword)}
            class="absolute inset-y-0 right-0 pr-3 text-gray-600"
          >
            {#if showConfirmPassword}
              <EyeOff class="h-5 w-5" />
            {:else}
              <Eye class="h-5 w-5" />
            {/if}
          </button>
        </div>
        {#if confirmPassword && !passwordsMatch}
          <p class="mt-2 text-sm text-red-600">Passwords do not match.</p>
        {/if}
      </div>

      <p>Already have account?
        <a href="/login" class="font-medium text-fg-brand hover:underline">Login</a>
      </p>

      <button
        type="submit"
        disabled={!passwordsMatch}
        class="w-full py-2 px-4 rounded-lg text-white bg-purple-600 hover:bg-purple-700 transition disabled:opacity-50 cursor-pointer"
      >
        Sign Up
      </button>
    </form>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
  }
</style>
