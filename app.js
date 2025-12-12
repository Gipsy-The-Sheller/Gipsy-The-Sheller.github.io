const { createApp, ref, computed, onMounted } = Vue;

createApp({
    setup() {
        const activeTab = ref('literature');
        const literatureSearch = ref('');
        const taxonomySearch = ref('');
        const sampleSearch = ref('');
        const loading = ref(false);
        const selected_item = ref(null);
        const selected_item_type = ref('');
        
        // 数据存储
        const literatureData = ref([]);
        const taxonomyData = ref([]);
        const sampleData = ref([]);

        const tabs = [
            { id: 'literature', name: '文献 (LITid)' },
            { id: 'taxonomy', name: '分类 (TAXid)' },
            { id: 'samples', name: '样本 (SMPid)' },
            { id: 'about', name: '关于' }
        ];

        // 获取文献数据
        const fetchLiterature = async () => {
            try {
                loading.value = true;
                const response = await fetch(`/api/literature?search=${encodeURIComponent(literatureSearch.value)}`);
                if (response.ok) {
                    literatureData.value = await response.json();
                } else {
                    console.error('获取文献数据失败:', response.status);
                }
            } catch (error) {
                console.error('获取文献数据出错:', error);
            } finally {
                loading.value = false;
            }
        };

        // 获取分类数据
        const fetchTaxonomy = async () => {
            try {
                loading.value = true;
                const response = await fetch(`/api/taxonomy?search=${encodeURIComponent(taxonomySearch.value)}`);
                if (response.ok) {
                    taxonomyData.value = await response.json();
                } else {
                    console.error('获取分类数据失败:', response.status);
                }
            } catch (error) {
                console.error('获取分类数据出错:', error);
            } finally {
                loading.value = false;
            }
        };

        // 获取样本数据
        const fetchSamples = async () => {
            try {
                loading.value = true;
                const response = await fetch(`/api/samples?search=${encodeURIComponent(sampleSearch.value)}`);
                if (response.ok) {
                    sampleData.value = await response.json();
                } else {
                    console.error('获取样本数据失败:', response.status);
                }
            } catch (error) {
                console.error('获取样本数据出错:', error);
            } finally {
                loading.value = false;
            }
        };

        // 生成ID
        const generateId = async (type) => {
            try {
                const response = await fetch(`/api/generate-id/${type}`);
                if (response.ok) {
                    const data = await response.json();
                    return data.id;
                } else {
                    console.error('生成ID失败:', response.status);
                    return null;
                }
            } catch (error) {
                console.error('生成ID出错:', error);
                return null;
            }
        };

        // 初始化数据获取
        onMounted(() => {
            fetchLiterature();
            fetchTaxonomy();
            fetchSamples();
        });

        // 监听搜索变化
        const onLiteratureSearch = () => {
            fetchLiterature();
        };

        const onTaxonomySearch = () => {
            fetchTaxonomy();
        };

        const onSampleSearch = () => {
            fetchSamples();
        };

        // 选中项目
        const selectItem = (item, type) => {
            selected_item.value = item;
            selected_item_type.value = type;
        };

        // 取消选中项目
        const deselectItem = () => {
            selected_item.value = null;
            selected_item_type.value = '';
        };

        // 过滤后的数据（保留作为备选方案）
        const filteredLiterature = computed(() => {
            return literatureData.value;
        });

        const filteredTaxonomy = computed(() => {
            return taxonomyData.value;
        });

        const filteredSamples = computed(() => {
            return sampleData.value;
        });

        return {
            activeTab,
            tabs,
            literatureSearch,
            taxonomySearch,
            sampleSearch,
            loading,
            selected_item,
            selected_item_type,
            filteredLiterature,
            filteredTaxonomy,
            filteredSamples,
            onLiteratureSearch,
            onTaxonomySearch,
            onSampleSearch,
            selectItem,
            deselectItem,
            generateId
        };
    }
}).mount('#app');
