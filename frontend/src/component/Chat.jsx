import { useState, useEffect } from "react";
import toast from 'react-hot-toast';
import axios from "axios";

export const Chat = () => {
    const [userInput, setUserInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [messages, setMessages] = useState([]);
    const [threadId, setThreadId] = useState();
    const initialMessage = "Hello, I'm Insurance Claims Assistant. I can help you with filiing claims, KYC rules, network hospitals etc."; // Keep your initial message here

    useEffect(() => {
        // Initialize with AI's first message
        setMessages([{
            text: initialMessage,
            isUser: false,
            displayedText: '',
            isTyping: true
        }]);
    }, []);

    // Typing effect controller
    useEffect(() => {
        const typingMessages = messages.filter(msg => msg.isTyping && msg.displayedText.length < msg.text.length);
        if (typingMessages.length > 0) {
            const timer = setTimeout(() => {
                setMessages(prev => prev.map(msg => {
                    if (msg.isTyping && msg.displayedText.length < msg.text.length) {
                        return {
                            ...msg,
                            displayedText: msg.text.slice(0, msg.displayedText.length + 1),
                            isTyping: msg.displayedText.length + 1 < msg.text.length
                        };
                    }
                    return msg;
                }));
            }, 20);

            return () => clearTimeout(timer);
        }
    }, [messages]);

    const askHandler = async () => {
        if (!userInput.trim()) {
            toast.error("No input provided.");
            return;
        }

        setIsLoading(true);
        
        try {
            // Add user message immediately
            setMessages(prev => [...prev, {
                text: userInput,
                isUser: true,
                displayedText: userInput,
                isTyping: false
            }]);


            const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/ask`, {
                query: userInput, 
                k:3,
                ...(threadId && { thread_id: threadId })
            });

            console.log(response.data.answer)

            setThreadId(response.data.thread_id)

            // Add AI response with typing effect
            setMessages(prev => [...prev, {
                text: response.data.answer,
                isUser: false,
                displayedText: '',
                isTyping: true
            }]);

            setUserInput("");
            toast.success("Response received!");
        } catch (err) {
            console.error("Error: ", err);
            toast.error("Something went wrong.");
        } finally {
            setIsLoading(false);
        }
    }


    return (
        <>
            <div className="mt-2 h-screen w-full flex justify-center">
                <div className="mt-2 w-full mx-4 md:w-[40%]">
                    <div className="w-full p-4 border border-gray-200 bg-gray-50 rounded-t-xl">
                        <div className="grid grid-cols-3">
                            <div className="col-span-3 text-center font-bold h-12">
                                Insurance Claim Assistant at your service.
                            </div>
                            {!threadId ? "" : <div className="col-span-3 text-center font-bold">
                                THREAD ID: {threadId}
                            </div>}
                        </div>
                    </div>
                    <div className="w-full h-[40%] overflow-y-auto p-4 border border-gray-200 bg-[radial-gradient(circle_800px_at_100%_0px,#faf0f9,transparent)]">
                        <div className="flex flex-col gap-4">
                            {messages.map((message, index) => (
                                <div 
                                    key={index}
                                    className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div className={`max-w-[80%] rounded-lg p-3 ${
                                        message.isUser 
                                            ? 'bg-cyan-600 text-white' 
                                            : 'bg-white text-gray-700 border'
                                    }`}>
                                        <div className="whitespace-pre-wrap">
                                            {message.displayedText}
                                            {message.isTyping && (
                                                <span className="ml-1 border-r-2 border-current animate-blink"></span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="w-full p-4 border border-gray-200 bg-gray-50 rounded-b-xl">
                        <div className="grid grid-cols-3">
                            <div className="col-span-2">
                                <textarea onChange={(e) => { setUserInput(userInput => e.target.value) }} id="message" rows="4" className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500" placeholder="What is the TAT for filing a claim?"></textarea>
                            </div>
                            <button onClick={askHandler} className="col-span-1 relative h-full items-center justify-center p-0.5 ml-2 overflow-hidden text-sm font-bold text-white rounded-lg group bg-gradient-to-br from-rose-400 to-slate-400 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white hover:cursor-pointer dark:text-white focus:ring-4 focus:outline-none focus:ring-blue-300">
                                {isLoading ? "" : "Send"}
                                <div role="status" className={`absolute ${!isLoading ? "hidden" : ""} -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2`}>
                                    <svg aria-hidden="true" className="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/><path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/></svg>
                                    <span className="sr-only">Loading...</span>
                                </div>
                            </button>

                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}