<script>
    import { Button } from '$ccs';

    let count = 0;
</script>

<div>
    <Button on:click={() => count++}>
        Clicked {count} {count === 1 ? 'time' : 'times'}
    </Button>
</div>
