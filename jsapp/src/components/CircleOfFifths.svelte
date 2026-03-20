<script>
    import { getPitchClassColor } from "../helper/coloring.js";

    const fifthsOrder = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5];
    const cx = 50;
    const cy = 50;
    const radius = 35;
</script>

<svg viewBox="0 0 100 100" width="70" height="70">
    <!-- Kreisparameter -->

    {#each fifthsOrder as pitch, i}
        <!-- 🔥 Start bei oben (C oben) -->
        {@const angle = (i / 12) * 2 * Math.PI - Math.PI / 2}

        {@const x = cx + Math.cos(angle) * radius}
        {@const y = cy + Math.sin(angle) * radius}

        <circle
            cx={x}
            cy={y}
            r="4"
            fill={getPitchClassColor(pitch, "meaningful_fifths")}
        />
    {/each}
</svg>

<style>
    svg {
        display: block;
    }
</style>
