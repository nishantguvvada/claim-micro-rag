export const Footer = () => {
    return (
        <>
            <footer className="fixed bottom-0 w-full bg-white rounded-lg shadow-xl m-4">
                <div className="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between">
                <span className="text-sm text-gray-500 sm:text-center dark:text-gray-400 font-serif">© 2025 <a className="font-serif hover:underline">claim-micro-rag.ai™</a>. All Rights Reserved.
                </span>
                <ul className="flex flex-wrap items-center mt-3 text-sm font-medium text-gray-500 dark:text-gray-400 sm:mt-0">
                    <li>
                        <a href="#" className="font-serif hover:underline me-4 md:me-6">About</a>
                    </li>
                    <li>
                        <a href="#" className="font-serif hover:underline me-4 md:me-6">Privacy Policy</a>
                    </li>
                    <li>
                        <a href="#" className="font-serif hover:underline me-4 md:me-6">Licensing</a>
                    </li>
                    <li>
                        <a href="#" className="font-serif hover:underline">Contact</a>
                    </li>
                </ul>
                </div>
            </footer>
        </>
    )
}