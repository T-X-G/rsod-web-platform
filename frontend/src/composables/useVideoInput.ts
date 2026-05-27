import { ref, type Ref } from "vue"

export function useVideoInput(videoSrc: Ref<string>) {
  const sourceType = ref<"file" | "url">("file")
  const videoUrl = ref("")
  const thumbnail = ref("")
  const errorMsg = ref("")
  const isLoading = ref(false)

  function handleFileSelect(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0]
    if (!file) return
    if (!file.type.startsWith("video/")) {
      errorMsg.value = "请选择视频文件"
      return
    }
    if (file.size > 200 * 1024 * 1024) {
      errorMsg.value = "视频文件超过 200MB，请先压缩"
      return
    }
    setFileSource(file)
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault()
    const file = event.dataTransfer?.files?.[0]
    if (!file) return
    if (!file.type.startsWith("video/")) { errorMsg.value = "请选择视频文件"; return }
    if (file.size > 200 * 1024 * 1024) { errorMsg.value = "视频文件超过 200MB"; return }
    setFileSource(file)
  }

  function setFileSource(file: File) {
    if (videoSrc.value.startsWith("blob:")) URL.revokeObjectURL(videoSrc.value)
    videoSrc.value = URL.createObjectURL(file)
    sourceType.value = "file"
    errorMsg.value = ""
    generateThumbnail()
  }

  function loadUrlVideo() {
    const url = videoUrl.value.trim()
    if (!url) { errorMsg.value = "请输入视频 URL"; return }
    if (!/^https?:\/\//i.test(url)) {
      errorMsg.value = "URL 需以 http:// 或 https:// 开头"
      return
    }
    if (videoSrc.value.startsWith("blob:")) URL.revokeObjectURL(videoSrc.value)
    videoSrc.value = url
    sourceType.value = "url"
    errorMsg.value = ""
  }

  function generateThumbnail() {
    const video = document.createElement("video")
    video.preload = "metadata"
    video.src = videoSrc.value
    video.onloadeddata = () => {
      video.currentTime = 0.5
      video.onseeked = () => {
        const c = document.createElement("canvas")
        c.width = video.videoWidth
        c.height = video.videoHeight
        c.getContext("2d")!.drawImage(video, 0, 0)
        thumbnail.value = c.toDataURL("image/jpeg", 0.3)
        video.remove()
      }
    }
    video.onerror = () => { video.remove() }
  }

  function handleDragOver(event: DragEvent) {
    event.preventDefault()
  }

  function reset() {
    if (videoSrc.value.startsWith("blob:")) URL.revokeObjectURL(videoSrc.value)
    videoSrc.value = ""
    thumbnail.value = ""
    errorMsg.value = ""
  }

  return {
    sourceType, videoUrl, thumbnail, errorMsg, isLoading,
    handleFileSelect, handleDrop, handleDragOver, loadUrlVideo, reset,
  }
}
