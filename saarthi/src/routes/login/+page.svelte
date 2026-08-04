<script>
  import { Eye, EyeOff, Mail, Lock, ArrowRight, ShieldCheck } from 'lucide-svelte'; 
  import { goto } from '$app/navigation';
  import { toast } from 'svelte-sonner';

  let email = '';
  let password = '';
  let showPassword = false;
  let error = "";

  async function handleLogin() {
    error = "";

    if (!email || !password) {
      error = "Email and Password required.";
      toast.error(error);
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem("user", JSON.stringify({
          name: data.name,
          email: data.email
        }));

        toast.success(`Welcome back, ${data.name || 'User'}!`);
        goto("/home");
      } else {
        error = data.detail || "Invalid login credentials.";
        toast.error(error);
      }
    } catch (e) {
      console.error("Login request error", e);
      toast.error("Unable to connect to login service.");
      goto("/home");
    }
  }
</script>

<div class="min-h-screen flex flex-col items-center justify-center p-4 relative z-10">
  <div class="w-full max-w-md bg-[#FFFFFF] p-8 rounded-3xl border border-[#D9DDD8] shadow-xl shadow-slate-200/50 space-y-8">
    
    <!-- Branding Header -->
    <div class="text-center space-y-3">
      <div class="flex justify-center mb-1">
        <img src="/images/logo.png" alt="Saarthi Logo" class="w-12 h-12 object-contain rounded-2xl shadow-sm" />
      </div>

      <h2 class="text-3xl font-extrabold text-[#1C1E1D] tracking-tight">
        Access <span class="text-[#2F7A5F]">Saarthi</span>
      </h2>
      <p class="text-[#646B67] text-sm">
        Sign in to your intelligent AI voice dashboard
      </p>
    </div>

    <form on:submit|preventDefault={handleLogin} class="space-y-5">
      <!-- Email Field -->
      <div class="space-y-1.5">
        <label for="email" class="block text-xs font-semibold text-[#1C1E1D] uppercase tracking-wider">
          Email Address
        </label>
        <div class="relative flex items-center">
          <Mail class="absolute left-4 w-5 h-5 text-[#646B67]" />
          <input
            type="email"
            id="email"
            bind:value={email}
            required
            class="w-full pl-12 pr-4 py-3 bg-[#F5F6F3] border border-[#D9DDD8] rounded-2xl focus:border-[#2F7A5F] focus:ring-1 focus:ring-[#2F7A5F] text-[#1C1E1D] placeholder-[#646B67] transition outline-none text-sm"
            placeholder="you@example.com"
          />
        </div>
      </div>

      <!-- Password Field -->
      <div class="space-y-1.5">
        <div class="flex items-center justify-between">
          <label for="password" class="block text-xs font-semibold text-[#1C1E1D] uppercase tracking-wider">
            Password
          </label>
          <a href="/forgot-password" class="text-xs text-[#2F7A5F] hover:text-[#26664E] font-medium transition">
            Forgot Password?
          </a>
        </div>
        <div class="relative flex items-center">
          <Lock class="absolute left-4 w-5 h-5 text-[#646B67]" />
          <input
            type={showPassword ? 'text' : 'password'}
            id="password"
            bind:value={password}
            required
            class="w-full pl-12 pr-12 py-3 bg-[#F5F6F3] border border-[#D9DDD8] rounded-2xl focus:border-[#2F7A5F] focus:ring-1 focus:ring-[#2F7A5F] text-[#1C1E1D] placeholder-[#646B67] transition outline-none text-sm"
            placeholder="••••••••"
          />
          <button
            type="button"
            on:click={() => (showPassword = !showPassword)}
            class="absolute right-4 text-[#646B67] hover:text-[#1C1E1D] transition"
          >
            {#if showPassword}
              <EyeOff class="h-4 w-4" />
            {:else}
              <Eye class="h-4 w-4" />
            {/if}
          </button>
        </div>
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        class="w-full py-3.5 px-4 rounded-2xl text-white font-semibold bg-[#2F7A5F] hover:bg-[#26664E] shadow-lg shadow-[#2F7A5F]/20 transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer group"
      >
        <span>Sign In to Workspace</span>
        <ArrowRight class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
      </button>

      <!-- Footer navigation -->
      <p class="text-center text-xs text-[#646B67] pt-2">
        Don't have an account yet?
        <a href="/signup" class="font-semibold text-[#2F7A5F] hover:text-[#26664E] transition underline underline-offset-4">Create Account</a>
      </p>
    </form>
  </div>
</div>