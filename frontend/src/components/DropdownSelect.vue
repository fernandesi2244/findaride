<template>
    <div :class="id">
        <input
            type="text"
            class="form-control select-form"
            placeholder="Start typing to see results..."
            @focus="focus"
            @input="search"
            v-model="input"
            :class="[isSelected ? 'is-valid' : '', id]"
        />
        <div v-show="isFocused" :class="id" style="position: relative; max-width: 100%;">
            <div :class="id" class="border-bottom list-group select-form" style="position: absolute; width: 100%; z-index: 1; padding: 0; margin: 0;">
                <button
                    type="button"
                    :class="id"
                    class="list-group-item list-group-item-action select-form"
                    v-for="suggestion in suggestions"
                    :value="suggestion.mapbox_id"
                    :key="suggestion.mapbox_id"
                    style="padding: 3px 5px 3px 8px;"
                    @click="selectLocation(suggestion)"
                >
                    <p class="text-truncate fw-bold mb-0" style="font-size: 14px; width: 100%;">{{ suggestion.name }}</p>
                    <p class="text-muted mb-0 text-truncate" style="font-size: 11px; width: 100%;">{{ suggestion.full_address }}</p>
                </button>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, defineProps, defineEmits, toRefs, onMounted } from 'vue';
import { axios } from '../common/axios_service.js'

const emit = defineEmits(['selectLocation']);
const props = defineProps(['id']);

const { id } = toRefs(props);

onMounted(() => {
    document.addEventListener("click", onClickOutside);
});

// ground truth data
const isFocused = ref(false);
const isSelected = ref(false);
const input = ref("");
const suggestions = ref([]);

function focus() {
    isFocused.value = true;
}

function onClickOutside(event) {
    if (!event.target.classList.contains(id.value)) {
        isFocused.value = false;
    }
}

async function selectLocation(suggestion) {
    input.value = suggestion.name;

    if (input.value.length == 0) {
        suggestions.value = [];
        return;
    }
    console.log(import.meta.env.VITE_MAPBOX_TOKEN)
    const url = `https://api.mapbox.com/search/searchbox/v1/retrieve/${suggestion.mapbox_id}?session_token=01e9d614-8fea-46e1-88d7-5f4c20f09fc8&access_token=${import.meta.env.VITE_MAPBOX_TOKEN}`;

    try {
        const results = await axios.get(url);
        emit('selectLocation', results.data.features[0].properties);
        isSelected.value = true;
    } catch (error) {
        alert(error);
    }
    isFocused.value = false;
}

async function search() {
    isSelected.value = false;
    if (input.value.length == 0) {
        suggestions.value = [];
        return;
    }

    const url = `https://api.mapbox.com/search/searchbox/v1/suggest?q=${input.value}&language=en&country=us&types=address,poi&session_token=07c99740-03dc-4261-88d7-1ca73f70b991&access_token=${import.meta.env.VITE_MAPBOX_TOKEN}`;

    try {
        const results = await axios.get(url);
        suggestions.value = results.data.suggestions;
    } catch (error) {
        alert(error);
    }
}
</script>