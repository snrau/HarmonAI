<script>
    let string = `this string contains some <strong>HTML!!!</strong>`;


    let count = $state(0);

    function increment() {
        // TODO implement
        count += 1;
    }

    let numbers = $state([1, 2, 3, 4]);
    let total = $derived(numbers.reduce((t, n) => t + n, 0));

    function addNumber() {
        numbers[numbers.length] = numbers.length + 1;
    }
</script>

<p>{@html string}</p>

<button onclick={increment}>
    Clicked {count}
    {count === 1 ? 'time' : 'times'}
</button>

<p>{numbers.join(' + ')} = {total}</p>

<button onclick={addNumber}>
    Add a number
</button>
