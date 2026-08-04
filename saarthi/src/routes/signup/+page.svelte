<script>
  import { Eye, EyeOff, User, Mail, Lock, ArrowRight, ShieldCheck, CheckCircle2 } from "lucide-svelte";
  import { goto } from "$app/navigation";
  import { toast } from "svelte-sonner";

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
      toast.error(error);
      return;
    }

    if (password.length < 6) {
      error = "Password must be at least 6 characters";
      toast.error(error);
      return;
    }

    if (password !== confirmPassword) {
      error = "Passwords do not match";
      toast.error(error);
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/api/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        error = data.detail || "Signup failed.";
        toast.error(error);
        return;
      }

      success = "Account created successfully!";
      toast.success("Account created successfully! Redirecting to login...");
      setTimeout(() => goto("/login"), 1000);
    } catch (e) {
      console.error("Signup error", e);
      error = "Network error while connecting to server.";
      toast.error(error);
    }
  }
</script>

<div class="min-h-screen flex flex-col items-center justify-center p-4 relative z-10">
  <div class="w-full max-w-lg bg-[#FFFFFF] p-8 rounded-3xl border border-[#D9DDD8] shadow-xl shadow-slate-200/50 space-y-7">
    
    <!-- Branding Header -->
    <div class="text-center space-y-3">
      <div class="flex justify-center mb-1">
        <img src="/images/logo.png" alt="Saarthi Logo" class="w-12 h-12 object-contain rounded-2xl shadow-sm" />
      </div>

      <h2 class="text-3xl font-extrabold text-[#1C1E1D] tracking-tight">
        Create Your <span class="text-[#2F7A5F]">Account</span>
      </h2>
      <p class="text-[#646B67] text-sm">
        Get instant access to your intelligent AI voice companion
      </p>
    </div>

    <form on:submit|preventDefault={handleSignup} class="space-y-4">
      <!-- Full Name -->
      <div class="space-y-1.5">
        <label for="name" class="block text-xs font-semibold text-[#1C1E1D] uppercase tracking-wider">
          Full Name
        </label>
        <div class="relative flex items-center">
          <User class="absolute left-4 w-5 h-5 text-[#646B67]" />
          <input
            type="text"
            id="name"
            bind:value={name}
            required
            class="w-full pl-12 pr-4 py-3 bg-[#F5F6F3] border border-[#D9DDD8] rounded-2xl focus:border-[#2F7A5F] focus:ring-1 focus:ring-[#2F7A5F] text-[#1C1E1D] placeholder-[#646B67] transition outline-none text-sm"
            placeholder="Jane Doe"
          />
        </div>
      </div>

      <!-- Email -->
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

      <!-- Password -->
      <div class="space-y-1.5">
        <label for="password" class="block text-xs font-semibold text-[#1C1E1D] uppercase tracking-wider">
          Password
        </label>
        <div class="relative flex items-center">
          <Lock class="absolute left-4 w-5 h-5 text-[#646B67]" />
          <input
            type={showPassword ? "text" : "password"}
            id="password"
            bind:value={password}
            required
            minlength="6"
            class="w-full pl-12 pr-12 py-3 bg-[#F5F6F3] border {passwordsMatch || password === '' ? 'border-[#D9DDD8] focus:border-[#2F7A5F]' : 'border-[#C45A4D]'} rounded-2xl focus:ring-1 focus:ring-[#2F7A5F] text-[#1C1E1D] placeholder-[#646B67] transition outline-none text-sm"
            placeholder="Min. 6 characters"
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

      <!-- Confirm Password -->
      <div class="space-y-1.5">
        <label for="confirm-password" class="block text-xs font-semibold text-[#1C1E1D] uppercase tracking-wider">
          Confirm Password
        </label>
        <div class="relative flex items-center">
          <Lock class="absolute left-4 w-5 h-5 text-[#646B67]" />
          <input
            type={showConfirmPassword ? "text" : "password"}
            id="confirm-password"
            bind:value={confirmPassword}
            required
            class="w-full pl-12 pr-12 py-3 bg-[#F5F6F3] border {confirmPassword && !passwordsMatch ? 'border-[#C45A4D]' : 'border-[#D9DDD8] focus:border-[#2F7A5F]'} rounded-2xl focus:ring-1 focus:ring-[#2F7A5F] text-[#1C1E1D] placeholder-[#646B67] transition outline-none text-sm"
            placeholder="Repeat password"
          />
          <button
            type="button"
            on:click={() => (showConfirmPassword = !showConfirmPassword)}
            class="absolute right-4 text-[#646B67] hover:text-[#1C1E1D] transition"
          >
            {#if showConfirmPassword}
              <EyeOff class="h-4 w-4" />
            {:else}
              <Eye class="h-4 w-4" />
            {/if}
          </button>
        </div>
        {#if confirmPassword && !passwordsMatch}
          <p class="text-xs text-[#C45A4D] font-medium pl-1">Passwords do not match.</p>
        {/if}
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        disabled={!passwordsMatch && confirmPassword !== ''}
        class="w-full mt-2 py-3.5 px-4 rounded-2xl text-white font-semibold bg-[#2F7A5F] hover:bg-[#26664E] shadow-lg shadow-[#2F7A5F]/20 transition-all duration-300 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 group"
      >
        <span>Create Free Account</span>
        <ArrowRight class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
      </button>

      <!-- Footer navigation -->
      <p class="text-center text-xs text-[#646B67] pt-2">
        Already have an account?
        <a href="/login" class="font-semibold text-[#2F7A5F] hover:text-[#26664E] transition underline underline-offset-4">Log In</a>
      </p>
    </form>
  </div>
</div>
